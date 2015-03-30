import random
import os
from django.http import Http404
from quiz_admin.models import Quiz, Files, Content
from reportlab.pdfgen import canvas
from io import BytesIO
from django.contrib.auth.models import User
from .models import Question, Choice
from django.http import HttpResponse
from user_data.models import Completed, UserAssignment
from .forms import UploadQuizData
from django.shortcuts import render
from BAGCA.settings import MEDIA_ROOT_FILES, AWS_S3_BUCKET_NAME
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from BAGCA.settings import MEDIA_ROOT
from .email_helpers import email
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from boto import s3
import threading
import datetime
import re


def get_training_page_content(request, training_id):
    try:
        quiz = Quiz.objects.get(pk=training_id)
        contents = Content.objects.filter(quiz_id=training_id)
    except Quiz.DoesNotExist:
        raise Http404

    training_info = {}
    content_list = []

    for content in contents:
        content_list.append(content)

    paginated_content = Paginator(content_list, 1)
    page = request.GET.get('page')

    try:
        training_info['content'] = paginated_content.page(page)
    except PageNotAnInteger:
        training_info['content'] = paginated_content.page(1)
    except EmptyPage:
        training_info['content'] = paginated_content.page(paginated_content.num_pages)

    training_info['title'] = quiz.quiz_name
    training_info['description'] = quiz.quiz_description
    training_info['id'] = training_id

    if paginated_content.num_pages > 1:
        paginate = True
    else:
        paginate = False

    context = {'training_info': training_info, 'paginate': paginate}

    return context


def get_mass_mail_return_page_context(request):
    quizzes_needed_to_be_completed = get_quizzes_needed_to_be_completed(request)

    result_set = get_users_groups_need_to_complete_quizzes(request)

    quizzes = set()
    groups = set()
    users = set()

    for result in result_set:
        value = result.split(':')
        quizzes.add(value[0])
        groups.add(value[1])
        users.add(value[2])

    context = {'quizzes_needed_to_be_completed': quizzes_needed_to_be_completed, 'users': users, 'groups': groups,
               'quizzes': quizzes}

    return context


def get_users_groups_need_to_complete_quizzes(request):
    all_quizzes = Quiz.objects.all()
    all_quiz_sets = set()

    for quiz in all_quizzes:
        for group in quiz.groups.all():
            for user in User.objects.filter(groups=group):
                all_quiz_sets.add(quiz.quiz_name + ":" + group.name + ":" + user.username)

    completed_quizzes = Completed.objects.all()
    completed_quiz_set = set()

    for completed in completed_quizzes:
        for group in completed.user.groups.all():
            completed_quiz_set.add(completed.quiz.quiz_name + ":" + group.name + ":" + completed.user.username)

    remaining_quizzes = all_quiz_sets.difference(completed_quiz_set)

    return remaining_quizzes


'''
def send_reminder_for_quiz(request):
    quiz_name = request.POST['quiz']

    quiz = Categories.objects.get(quiz_name=quiz_name)

    for group in quiz.groups.all():
        request.POST._mutable = True
        request.POST['group'] = group
        request.POST['user'] = request.user.username
        send_reminder_to_group(request)
        #send_reminder_to_group_thread = threading.Thread(target=send_reminder_to_group(request), args=request)
        #send_reminder_to_group_thread.start()

    context = get_mass_mail_return_page_context(request)

    return render(request, "check_user_status.html", context)
'''

'''
    try:
        requested_quiz = request.POST['quiz']
        requested_group = request.POST['group']

        for group in user.groups.all():
            for quiz in Categories.objects.filter(groups=group):
                #if quiz.quiz_name == requested_quiz and group.name == requested_group:
                assigned_quizzes.add(quiz)
    except KeyError:
'''


def send_reminder_to_group(request):
    group_name = request.POST['group']

    group = Group.objects.get(name=group_name)

    users = User.objects.filter(groups=group)

    for user in users:
        request.POST._mutable = True
        request.POST['user'] = user
        send_reminder_to_user_thread = threading.Thread(target=send_reminder_to_user(request), args=request)
        send_reminder_to_user_thread.start()

    context = get_mass_mail_return_page_context(request)

    return render(request, "check_user_status.html", context)


def send_reminder_to_user(request):
    username = request.POST['user']

    user = User.objects.get(username=username)

    assigned_quizzes = set()

    try:
        requested_group = request.POST['group']
        for group in user.groups.all():
            for quiz in Quiz.objects.filter(groups=group):
                if group.name == requested_group:
                    assigned_quizzes.add(quiz)
    except KeyError:
        for group in user.groups.all():
            for quiz in Quiz.objects.filter(groups=group):
                assigned_quizzes.add(quiz)

    completed_quizzes = set()
    for completed in Completed.objects.filter(user=user):
        completed_quizzes.add(completed.quiz)

    remaining_quizzes = assigned_quizzes.difference(completed_quizzes)

    if len(remaining_quizzes) >= 1:
        email_thread = threading.Thread(target=send_mass_mail(request, user, remaining_quizzes),
                                        args=[request, user, remaining_quizzes])

        email_thread.start()

    context = get_mass_mail_return_page_context(request)

    return render(request, "check_user_status.html", context)


def send_mass_mail(request, user, remaining_quizzes):
    subject = "Please complete the quizzes listed below."

    message = "Hello " + user.first_name + ",\n\n"
    for quiz in remaining_quizzes:
        message += "You need to complete quiz '" + quiz.quiz_name + "' by " + str(quiz.due_date) + "\n"

    message += "\n\nThank you,\nBoys and Girls Club"
    email(request, subject, message, user.email)

    return HttpResponse(user.username + " " + str(remaining_quizzes))


def send_reminder_mail(request):
    quiz = Quiz.objects.get(pk=request.POST['quiz_id'])
    subject = 'You need to complete "' + str(quiz.quiz_name) + '" by ' + str(quiz.due_date) + '.'
    message = ''

    user = User.objects.get(username=request.POST['user'])

    email(request, subject, message, user.email)

    alert_msg = "Email has been successfully sent to: " + str(user.username) + " (" + str(user.email) + ")"
    alert_style = "alert-success"

    quizzes_needed_to_be_completed = get_quizzes_needed_to_be_completed(request)

    need_to_send_mail = set()

    for send_mail_for_quiz in quizzes_needed_to_be_completed:
        if quiz.id != send_mail_for_quiz.id:
            need_to_send_mail.add(send_mail_for_quiz)

    context = {'alert_msg': alert_msg, 'alert_style': alert_style,
               'quizzes_needed_to_be_completed': need_to_send_mail}
    return render(request, 'check_user_status.html', context)


def get_quizzes_needed_to_be_completed(request):
    quizzes = Quiz.objects.all()
    quiz_set = set()

    for quiz in quizzes:
        quiz_set.add(quiz)

    completed_by_user = Completed.objects.filter(user=request.user)
    completed_by_user_set = set()

    for completed_quizzes in completed_by_user:
        completed_by_user_set.add(completed_quizzes.quiz)

    quizzes_needed_to_be_completed = quiz_set.difference(completed_by_user_set)

    return quizzes_needed_to_be_completed


def add_groups(request):
    groups = request.POST.getlist('groups')

    for group in groups:
        quiz_group = Group.objects.get(name=group)
        quiz_group.user_set.add(request.user)

    return HttpResponseRedirect("/")


def get_user_assigned_trainings(request):
    user_assignments = UserAssignment.objects.filter(user=request.user)
    user_assigned = set()

    for assignment in user_assignments:
        user_assigned.add(assignment.quiz)

    return user_assigned


def get_admin_assigned_trainings(request):
    user_groups = []
    display_groups = set()
    trainings_need_to_be_completed = set()

    for groups in request.user.groups.all():
        user_groups.append(groups)
        for available_trainings in Quiz.objects.filter(groups=groups):
            display_groups.add(available_trainings.id)

    for quiz_id in display_groups:
        check_if_user_finished_quiz = Completed.objects.filter(quiz=quiz_id, user=request.user)
        quiz_name = Quiz.objects.get(pk=quiz_id)
        if not check_if_user_finished_quiz:
            trainings_need_to_be_completed.add(quiz_name)

    return trainings_need_to_be_completed


def download_file(request, file_id):
    database_file_object = Files.objects.get(pk=file_id)

    database_file_object_string = str(database_file_object.file)

    out_filename = re.match(r'.*/(.*)', database_file_object_string, re.M | re.I)

    out_file = out_filename.groups(1)[0]

    file_extension = re.match(r'.*\.(.*)', out_file, re.M | re.I)

    response = HttpResponse(content_type=file_extension.groups(1))
    response["Content-Disposition"] = "attachment; filename=" + out_file + ""

    filepath = Files.object.get(pk=file_id)

    '''
    url = s3.generate_url(60, 'GET',
                          bucket=AWS_S3_BUCKET_NAME,
                          key=filepath,
                          response_headers=response,
                          force_http=True)
    '''

    response_file_object = open(s3._open(filepath.file))

    for line in response_file_object:
        response.write(line)

    return response


def create_quiz_form(request):
    if request.method == 'POST':
        form = UploadQuizData(request.POST, request.FILES)
        if form.is_valid():

            filename = "temporary_file.txt"
            fd = open('%s/%s' % (MEDIA_ROOT_FILES, filename), 'wb')

            group = request.POST['group_choices']
            quiz_name = request.POST['quiz_name']
            trainer = request.POST['trainer']
            quiz_description = request.POST['quiz_description']
            course_code = request.POST['course_code']
            due_date = request.POST['due_date']
            duration_hours = request.POST['duration_hours']
            required_score = request.POST['required_score']

            determine_if_quiz_exists = Quiz.objects.filter(quiz_name=quiz_name)

            if not determine_if_quiz_exists:
                create_quiz = Quiz(quiz_name=quiz_name,
                                   quiz_description=quiz_description,
                                   trainer=trainer,
                                   course_code=course_code,
                                   due_date=due_date,
                                   duration_hours=duration_hours,
                                   required_score=required_score)
                create_quiz.save()
                create_quiz.groups.add(group)
                quiz_id = Quiz.objects.get(quiz_name=quiz_name)

                for line in request.FILES['file'].read():
                    fd.write(line)

                fd.close()

                written_file = open(MEDIA_ROOT_FILES + '/temporary_file.txt', 'r')

                for line in written_file:
                    parts = re.split(r'\t', line)

                    create_question = Question(quiz=quiz_id, question_text=parts[0])
                    create_question.save()
                    for part_counter in range(1, len(parts)):
                        is_answer = False
                        parts[part_counter] = parts[part_counter].strip()
                        if parts[part_counter][0] == '(' and \
                                        parts[part_counter][len(parts[part_counter]) - 1] == ')':
                            parts[part_counter] = parts[part_counter][1:len(parts[part_counter]) - 1]
                            is_answer = True

                        create_choice = Choice(question=Question.objects.get(pk=create_question.id),
                                               choice_text=parts[part_counter].strip(), answer=is_answer)
                        create_choice.save()

                fd.close()
                os.remove(MEDIA_ROOT_FILES + '/temporary_file.txt')
                form = UploadQuizData()
                data = {'form': form}
                return render(request, 'create_quiz_form.html', data)

    else:
        form = UploadQuizData()

    data = {'form': form}
    return render(request, 'create_quiz_form.html', data)


def get_questions_for_quiz(training_id):
    try:
        latest_question_list = sorted(Question.objects.filter(quiz=training_id),
                                      key=lambda random_key: random.random())
    except Question.DoesNotExist:
        raise Http404

    question_dictionary = {}
    for q in latest_question_list:
        question_dictionary[q] = sorted(q.choice_set.all(), key=lambda random_key: random.random())

    return question_dictionary


def print_quiz(request, training_id):
    response = HttpResponse(content_type='text/plain')
    quiz = Quiz.objects.get(pk=training_id)
    response["Content-Disposition"] = "attachment; filename=" + re.sub(r"\s+", "_", quiz.quiz_name) + "_quiz.txt"

    question_dictionary = get_questions_for_quiz(training_id)

    question_number = 1
    for question in question_dictionary:
        response.write(str(question_number) + ") " + question.question_text + "\n")

        for choice in question_dictionary[question]:
            response.write("   - " + choice.choice_text + "\n")

        question_number += 1
        response.write("\n")

    return response


def get_current_quiz(training_id):
    return Quiz.objects.get(pk=training_id)


def save_user_completion(request, training_id):
    current_quiz = get_current_quiz(training_id)

    # Store the results of the user in the database; also allow admins to correct any mistakes.
    check_if_user_finished_quiz = Completed.objects.filter(quiz=current_quiz, user=request.user,
                                                           date_completed=datetime.date.today())

    if not check_if_user_finished_quiz:
        store_result = Completed(quiz=current_quiz, user=request.user, date_completed=datetime.date.today())
        store_result.save()


def save_user_assignment(request, training_id):
    # Store the results of the user in the database; also allow admins to correct any mistakes.
    training = Quiz.objects.get(pk=training_id)
    check_if_user_assigned_quiz = UserAssignment.objects.filter(quiz=training, user=request.user)

    if not check_if_user_assigned_quiz:
        store_assignment = UserAssignment(quiz=training, user=request.user)
        store_assignment.save()
        return "added"

    return "exists"


def determine_pass_or_fail(correct_answers, total_number_of_questions, required_score):
    score = int((float(correct_answers) / total_number_of_questions) * 100)

    if score >= required_score:
        return True, score
    else:
        return False, score


def get_result_page_styling(correct_answers, total_number_of_questions, required_score):
    result, score = determine_pass_or_fail(correct_answers, total_number_of_questions, required_score)
    if result:
        return "passed", "green", score
    else:
        return "failed", "red", score


def set_certificate_properties(pdf):
    image_top = canvas.ImageReader(MEDIA_ROOT + '/Certificate_top.tiff')  # image_data is a raw string containing a JPEG
    pdf.drawImage(image_top, 0, 470, 600, 400)

    image_bottom = canvas.ImageReader(
        MEDIA_ROOT + '/Certificate_bottom.tiff')  # image_data is a raw string containing a JPEG
    pdf.drawImage(image_bottom, 0, 100, 600, 75)
    pdf.line(300, 90, 550, 90)
    pdf.setLineWidth(.5)

    # Add the outer borders; vertical lines
    pdf.line(10, 830, 10, 10)
    pdf.line(585, 830, 585, 10)

    # Add the inner borders; vertical lines
    pdf.line(15, 825, 15, 15)
    pdf.line(580, 825, 580, 15)

    # Add the outer borders; horizontal lines
    pdf.line(10, 10, 585, 10)
    pdf.line(10, 830, 585, 830)

    # Add the inner borders; horizontal lines
    pdf.line(15, 15, 580, 15)
    pdf.line(15, 825, 580, 825)

    return pdf


def generate_certificate(request, training_id):
    quiz = Quiz.objects.get(pk=training_id)
    user = User.objects.get(username=request.user.username)
    completed = Completed.objects.get(quiz=quiz, user=user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate_of_completion.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    pdf = canvas.Canvas(buffer)
    pdf.setFont('Helvetica', 15)
    pdf.drawString(245, 450, "This certifies that")
    pdf.setFont('Helvetica', 30)

    user_first_last_name = request.user.first_name + " " + request.user.last_name

    if user_first_last_name.strip() == '':
        user_first_last_name = request.user.email.split("@")[0]

    user_name_length = len(user_first_last_name) * 7

    pdf.drawString(290 - user_name_length, 400, user_first_last_name)

    pdf.line(105, 395, 525, 395)
    # message = "has completed " + str(quiz.duration_hours) + " hours of training."

    # pdf.drawString(175 - len(message) / 2, 380, message)
    pdf.setFont('Helvetica', 15)

    pdf.drawString(205, 350, "has successfully completed the course:")
    course_and_course_code = quiz.quiz_name + "(" + quiz.course_code + ")"
    pdf.drawString(335 - (len(course_and_course_code) * 5), 325, course_and_course_code)
    pdf.drawString(220, 300, "This course is worth " + str(quiz.duration_hours) + " of training.")
    pdf.drawString(245, 270, "Issued: " + str(completed.date_completed))

    pdf.drawString(165, 240, "Issuing body: Boys & Girls Clubs of Delaware")

    pdf.setFont('Helvetica', 12)
    pdf.drawString(300, 70, "Trainer: " + quiz.trainer)

    set_certificate_properties(pdf)

    # Close the PDF object cleanly.
    pdf.showPage()
    pdf.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
