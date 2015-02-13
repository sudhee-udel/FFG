import random
from django.http import Http404
from quiz_admin.models import Categories
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import Question
from django.http import HttpResponse
from user_data.models import Completed
from .forms import UploadQuizData
from django.http import HttpResponseRedirect
from django.shortcuts import render


def create_quiz_form(request):
    if request.method == 'POST':
        form = UploadQuizData(request.POST, request.FILES)
        if form.is_valid():
            response = HttpResponse(content_type='text/plain')
            response["Content-Disposition"]= "attachment; filename=quiz.txt"
            for line in request.FILES['file'].read():
                response.write(line)

            return response
    else:
        form = UploadQuizData()

    data = {'form': form}
    return render(request, 'create_quiz_form.html', data)

def create_quiz(file):
    response = HttpResponse(content_type='text/plain')
    response["Content-Disposition"]= "attachment; filename=quiz.txt"

    for line in file.read():
        response.write(line)

    return response

def get_questions_for_quiz(training_id):
    try:
        latest_question_list = sorted(Question.objects.filter(category=training_id), key=lambda random_key: random.random())
    except Question.DoesNotExist:
        raise Http404

    question_dictionary = {}
    for q in latest_question_list:
        question_dictionary[q] = sorted(q.choice_set.all(), key=lambda random_key: random.random())

    return question_dictionary

def print_quiz(request, training_id):
    response = HttpResponse(content_type='text/plain')
    quiz = Categories.objects.get(pk=training_id)
    response["Content-Disposition"]= "attachment; filename=" + quiz.category_text + "_quiz.txt"

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
    check_if_user_finished_quiz = Completed.objects.filter(category=training_id,user=request.user.email)

    if not check_if_user_finished_quiz:
        store_result = Completed(category=training_id, user=request.user.email)
        store_result.save()

def determine_pass_or_fail(correct_answers, total_number_of_questions, required_score):
    score = int((float(correct_answers)/total_number_of_questions) * 100)

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
    image = canvas.ImageReader('quizzes/BAGCA.jpg') # image_data is a raw string containing a JPEG

    pdf.drawImage(image, 100, 600, 400, 200)
    pdf.setLineWidth(.5)

    # Add the outer borders; vertical lines
    pdf.line(10,830,10,10)
    pdf.line(585,830,585,10)

    # Add the inner borders; vertical lines
    pdf.line(15,825,15,15)
    pdf.line(580,825,580,15)

    # Add the outer borders; horizontal lines
    pdf.line(10,10,585,10)
    pdf.line(10,830,585,830)

    # Add the inner borders; horizontal lines
    pdf.line(15,15,580,15)
    pdf.line(15,825,580,825)

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

    user_name_length = len(user_first_last_name)/2
    pdf.drawString(250 - user_name_length, 410, user_first_last_name)
    pdf.setFont('Helvetica', 20)

    message = "has completed " + str(category.duration_hours) + " hours of training."

    pdf.drawString(175 - len(message)/2, 380, message)

    set_certificate_properties(pdf)

    # Close the PDF object cleanly.
    pdf.showPage()
    pdf.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response