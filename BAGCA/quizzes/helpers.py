import random
from django.http import Http404
from quiz_admin.models import Categories
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import Question, Choice
from django.http import HttpResponse
from user_data.models import Completed
from .forms import UploadQuizData
from django.shortcuts import render
from BAGCA.settings import MEDIA_ROOT_FILES
from django.contrib.auth.models import Group
import uuid
import re


def create_quiz_form(request):
    quiz_groups = Group.objects.all()
    if request.method == 'POST':
        form = UploadQuizData(request.POST, request.FILES)
        if form.is_valid():
            filename = "temporary_file.txt" #str(uuid.uuid1()) + "_" + request.FILES['file'].name
            fd = open('%s/%s' % (MEDIA_ROOT_FILES, filename), 'wb')

            category_text = request.POST['category_text']
            category_description = request.POST['category_description']
            course_code = request.POST['course_code']
            due_date = request.POST['due_date']
            duration_hours = request.POST['duration_hours']
            required_score = request.POST['required_score']

            create_quiz = Categories(category_text=category_text,
                                     category_description=category_description,
                                     course_code=course_code,
                                     due_date=due_date,
                                     duration_hours=duration_hours,
                                     required_score=required_score)
            create_quiz.save()

            quiz_id = Categories.objects.get(category_text=category_text)
            list = []
            # fd.write(category_text + "\n" + category_description + "\n" + course_code + "\n" + str(due_date) + "\n" + str(duration_hours) + "\n" + str(required_score) + "\n")
            for line in request.FILES['file'].read():
                fd.write(line)
                list.append(line)
                #create_question = Question(category=quiz_id, question_text=parts[0])
                #create_question.save()

            fd.close()

            written_file = open(MEDIA_ROOT_FILES + '/temporary_file.txt')

            new_fd = open('%s/%s' % (MEDIA_ROOT_FILES, "new_question_" + filename), 'wb')
            new_fd1 = open('%s/%s' % (MEDIA_ROOT_FILES, "new_choice_" + filename), 'wb')
            for line in written_file:
                parts = line.split('\t')
                new_fd.write(parts[0])
                create_question = Question(category=quiz_id, question_text=parts[0])
                create_question.save()
                for part_counter in range(1, len(parts)):
                    is_answer = False
                    if (parts[part_counter][0] == '(') and (parts[part_counter][len(parts[part_counter]) - 1] == ')'):
                        parts[part_counter] = parts[part_counter][1:len(parts[part_counter]) - 1]
                        is_answer = True
                    create_choice = Choice(question=Question.objects.get(pk=create_question.id), choice_text=parts[part_counter], answer=is_answer)
                    create_choice.save()
                    new_fd1.write(parts[part_counter] + str(create_question.id) + "\n")

            fd.close()

    else:
        form = UploadQuizData()

    data = {'form': form, 'groups': quiz_groups}
    return render(request, 'create_quiz_form.html', data)


def create_quiz(request, file):
    fd = open('%s/%s' % (MEDIA_ROOT_FILES, str(uuid.uuid1()) + "_" + request.FILES['file'].name), 'wb')

    for line in request.FILES['file'].read():
        fd.write(line)

    fd.close()
    response = HttpResponse(content_type='text/plain')
    response["Content-Disposition"] = "attachment; filename=quiz.txt"

    for line in request.FILES['file'].read():
        response.write(line)

    return response


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