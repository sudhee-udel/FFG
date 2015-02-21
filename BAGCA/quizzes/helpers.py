import random
import os
from django.http import Http404
from quiz_admin.models import Categories, Files
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import Question, Choice
from django.http import HttpResponse
from user_data.models import Completed, UserAssignment
from .forms import UploadQuizData
from django.shortcuts import render
from BAGCA.settings import MEDIA_ROOT_FILES
from django.contrib.auth.models import Group
import re


def get_user_assigned_trainings(request):
    user_assignments = UserAssignment.objects.filter(user=request.user)
    user_assigned = set()

    for assignment in user_assignments:
        user_assigned.add(assignment.category)

    return user_assigned


def get_admin_assigned_trainings(request):
    user_groups = []
    display_groups = set()
    trainings_need_to_be_completed = set()

    for groups in request.user.groups.all():
        user_groups.append(groups)
        for available_trainings in Categories.objects.filter(groups=groups):
            display_groups.add(available_trainings.id)

    for quiz_id in display_groups:
        check_if_user_finished_quiz = Completed.objects.filter(category=quiz_id, user=request.user.email)
        quiz_name = Categories.objects.get(pk=quiz_id)
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

    response_file_object = open(MEDIA_ROOT_FILES + '/' + out_file, 'r')

    for line in response_file_object:
        response.write(line)

    return response


def create_quiz_form(request):
    quiz_groups = Group.objects.all()
    if request.method == 'POST':
        form = UploadQuizData(request.POST, request.FILES)
        if form.is_valid():
            filename = "temporary_file.txt"
            fd = open('%s/%s' % (MEDIA_ROOT_FILES, filename), 'wb')

            category_text = request.POST['category_text']
            category_description = request.POST['category_description']
            course_code = request.POST['course_code']
            due_date = request.POST['due_date']
            duration_hours = request.POST['duration_hours']
            required_score = request.POST['required_score']

            determine_if_quiz_exists = Categories.objects.filter(category_text=category_text)

            if not determine_if_quiz_exists:
                create_quiz = Categories(category_text=category_text,
                                         category_description=category_description,
                                         course_code=course_code,
                                         due_date=due_date,
                                         duration_hours=duration_hours,
                                         required_score=required_score)
                create_quiz.save()

                quiz_id = Categories.objects.get(category_text=category_text)

                for line in request.FILES['file'].read():
                    fd.write(line)

                fd.close()

                written_file = open(MEDIA_ROOT_FILES + '/temporary_file.txt', 'r')

                for line in written_file:
                    parts = line.split('\t')

                    create_question = Question(category=quiz_id, question_text=parts[0])
                    create_question.save()
                    for part_counter in range(1, len(parts)):
                        is_answer = False

                        if (parts[part_counter][0] == '(') and (
                                    parts[part_counter][len(parts[part_counter]) - 1] == ')'):
                            parts[part_counter] = parts[part_counter][1:len(parts[part_counter]) - 1]
                            is_answer = True

                        create_choice = Choice(question=Question.objects.get(pk=create_question.id),
                                               choice_text=parts[part_counter], answer=is_answer)
                        create_choice.save()

                fd.close()
                os.remove(MEDIA_ROOT_FILES + '/temporary_file.txt')

    else:
        form = UploadQuizData()

    data = {'form': form, 'groups': quiz_groups}
    return render(request, 'create_quiz_form.html', data)


def get_questions_for_quiz(training_id):
    try:
        latest_question_list = sorted(Question.objects.filter(category=training_id),
                                      key=lambda random_key: random.random())
    except Question.DoesNotExist:
        raise Http404

    question_dictionary = {}
    for q in latest_question_list:
        question_dictionary[q] = sorted(q.choice_set.all(), key=lambda random_key: random.random())

    return question_dictionary


def print_quiz(request, training_id):
    response = HttpResponse(content_type='text/plain')
    quiz = Categories.objects.get(pk=training_id)
    response["Content-Disposition"] = "attachment; filename=" + quiz.category_text + "_quiz.txt"

    question_dictionary = get_questions_for_quiz(training_id)

    question_number = 1
    for question in question_dictionary:
        response.write(str(question_number) + ") " + question.question_text + "\n")

        for choice in question_dictionary[question]:
            response.write("   - " + choice.choice_text + "\n")

        question_number += 1
        response.write("\n")

    return response


def save_user_completion(request, training_id):
    # Store the results of the user in the database; also allow admins to correct any mistakes.
    check_if_user_finished_quiz = Completed.objects.filter(category=training_id, user=request.user.email)

    if not check_if_user_finished_quiz:
        store_result = Completed(category=training_id, user=request.user.email)
        store_result.save()


def save_user_assignment(request, training_id):
    # Store the results of the user in the database; also allow admins to correct any mistakes.
    training = Categories.objects.get(pk=training_id)
    check_if_user_assigned_quiz = UserAssignment.objects.filter(category=training, user=request.user)

    if not check_if_user_assigned_quiz:
        store_assignment = UserAssignment(category=training, user=request.user)
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
    image = canvas.ImageReader('quizzes/BAGCA.jpg')  # image_data is a raw string containing a JPEG

    pdf.drawImage(image, 100, 600, 400, 200)
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
    category = Categories.objects.get(pk=training_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate_of_completion.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    pdf = canvas.Canvas(buffer)

    pdf.setFont('Helvetica', 30)

    user_first_last_name = request.user.first_name + " " + request.user.last_name

    if user_first_last_name.strip() == '':
        user_first_last_name = request.user.email.split("@")[0]

    user_name_length = len(user_first_last_name) / 2
    pdf.drawString(250 - user_name_length, 410, user_first_last_name)
    pdf.setFont('Helvetica', 20)

    message = "has completed " + str(category.duration_hours) + " hours of training."

    pdf.drawString(175 - len(message) / 2, 380, message)

    set_certificate_properties(pdf)

    # Close the PDF object cleanly.
    pdf.showPage()
    pdf.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
