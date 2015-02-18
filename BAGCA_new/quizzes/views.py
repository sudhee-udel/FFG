import time

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from quizzes.models import Question, Choice
from quiz_admin.models import Categories, Videos
from user_data.models import Completed
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader, Image
import StringIO
from io import BytesIO
import re

@login_required
def index(request):
    user_groups = []
    display_groups = set()
    trainings_need_to_be_completed = set()

    for groups in request.user.groups.all():
        user_groups.append(groups)
        for available_trainings in Categories.objects.filter(groups=groups):
            display_groups.add(available_trainings.id)

    for quiz_id in display_groups:
        check_if_user_finished_quiz = Completed.objects.filter(category=quiz_id,user=request.user.email)
        quiz_name = Categories.objects.get(pk=quiz_id)
        if not check_if_user_finished_quiz:
            trainings_need_to_be_completed.add(quiz_name)

    context = {'trainings': sorted(trainings_need_to_be_completed, key=str)}
    return render(request, 'index.html', context)

@login_required
def profile(request):
    if request.method == 'GET':

        return render(request, 'profile.html', {})

    elif request.method == 'POST':
        user = request.user
        user.email = request.POST['email']
        user.save

        context = {}

        return render(request, 'profile.html', context)
    

@login_required
def training(request, training_id):
    try:
        category = Categories.objects.get(pk=training_id)
        videos = Videos.objects.filter(category_id=training_id)
    except Categories.DoesNotExist:
        raise Http404

    training_info = {}
    video_list = []

    for video in videos:
        video_list.append(video)

    training_info['videos'] = video_list
    training_info['title']= category.category_text
    training_info['description'] = category.category_description
    training_info['id'] = training_id
    training_info['training_text'] = category.training_text
    training_info['duration'] = category.duration_hours

    context = {'training_info': training_info}
    return render(request, 'trainings/training.html', context)

@login_required
def quiz(request, training_id):
    if request.method == 'GET':
        try:
            latest_question_list = Question.objects.filter(category=training_id)
            #latest_question_list = Question.objects.order_by('question_text')[:]
        except Question.DoesNotExist:
            raise Http404

        question_dictionary = {}
        for q in latest_question_list:
            question_dictionary[q] = q.choice_set.all()

        return render(request, 'trainings/quiz.html', {'question_dictionary': question_dictionary, 'training_id': training_id, 'count': len(question_dictionary)})

    elif request.method == 'POST':
        questionList = []
        for value in request.POST:
            if 'question' in value:
                questionList.append(value)

        result_msg, correct, count = get_formatted_message(request.POST, questionList)    
        print result_msg
        print "training_id: " + str(training_id)
        print "correct: " + str(correct)
        print "count: " + str(count)

        score = int((float(correct)/float(count)) * 100)
        category = Categories.objects.get(pk=training_id)
        result = ""

        if score>=category.required_score:        
            result = "passed"
            color = "green"
        else:
            result = "failed"             
            color = "red"
        if result == 'passed':
            # Store the results of the user in the database; also allow admins to correct any mistakes.
            check_if_user_finished_quiz = Completed.objects.filter(category=training_id,user=request.user.email)
            if not check_if_user_finished_quiz:
                store_result = Completed(category=training_id, user=request.user.email)
                store_result.save()

            # Send the mail to users, if they have passed the quiz
            subject = "You have finished the " + category.category_text + " quiz."
            message = "You have passed!\n\nPlease retain this message for your records."
            email(request, subject, message)

        context = {'result':result, 'result_msg':result_msg, 'correct':correct, 'count':count, 'score':score, 'color':color, 'training_id':training_id, 'required_score':category.required_score}

        return render(request, 'trainings/results.html', context)

@login_required
def results(request, training_id):
    return render(request, 'quizzes/results.html', {})

# ***** this should probably go in a helper class
def pdfs(request, training_id):
    category = Categories.objects.get(pk=training_id)
    # Create the HttpResponse object with the appropriate PDF headers.
    image = canvas.ImageReader('quizzes/BAGCA.jpg') # image_data is a raw string containing a JPEG

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate_of_completion.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    p.setLineWidth(.5)
    p.setFont('Helvetica', 30)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawImage(image, 100, 600, 400, 200)

    user_first_last_name = request.user.first_name + " " + request.user.last_name

    if user_first_last_name.strip() == '':
        user_first_last_name = request.user.email.split("@")[0]

    user_name_length = len(user_first_last_name)/2
    p.drawString(250 - user_name_length, 410, user_first_last_name)
    p.setFont('Helvetica', 20)

    message = "has completed " + str(category.duration_hours) + " hours of training."

    p.drawString(175 - len(message)/2, 380, message)

    #Add the outer borders; vertical lines
    p.line(10,830,10,10)
    p.line(585,830,585,10)

    #Add the inner borders; vertical lines
    p.line(15,825,15,15)
    p.line(580,825,580,15)

    #Add the outer borders; horizontal lines
    p.line(10,10,585,10)
    p.line(10,830,585,830)

    #Add the inner borders; horizontal lines
    p.line(15,15,580,15)
    p.line(15,825,580,825)

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

# ***** this should probably go in a helper class
def get_formatted_message(post_data, questionList):
    message = []
    count = 0
    correct = 0

    for item in sorted(questionList):
        count += 1
        question_re = re.match(r'question_(.*)', item, re.M)
        choice_value = Choice.objects.get(pk=post_data.get(item, ''))
        choice_result = 'wrong.'
        if choice_value.answer:
            correct += 1
            choice_result = 'correct.'
        message.append("For question: " + str(Question.objects.get(pk=question_re.groups(1)[0])) + " You chose: " + str(choice_value) + ". It is " + choice_result + "\n")

    return message, correct, count

# ***** this should probably go in a helper class
# this method currently does not link to anything. will be used to send email.
def email(request, subject, message):
    if request.method == 'POST':
        list = []

        for value in request.POST:
            if 'question' in value:
                list.append(value)

        send_mail(subject, message, 'chas.barnajr@tsgforce.com', [request.user.email], fail_silently=False)

    return
