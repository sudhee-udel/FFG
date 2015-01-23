import time

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from quizzes.models import Question, Choice
from quiz_admin.models import Categories
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader, Image
import StringIO
from io import BytesIO
import re

@login_required
def index(request):
    trainings = Categories.objects.order_by('category_text')[:]
    context = {'trainings': trainings}
    return render(request, 'index.html', context)

@login_required
def training(request, training_id):
    try:
        category = Categories.objects.get(pk=training_id)
    except Categories.DoesNotExist:
        raise Http404

    training_info = {}
    training_info['url'] = category.url
    training_info['text']= category.category_text
    training_info['id'] = training_id

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
 
        context = {'result':result, 'result_msg':result_msg, 'correct':correct, 'count':count, 'score':score, 'color':color}

        return render(request, 'trainings/results.html', context)

@login_required
def results(request, training_id):
    return render(request, 'quizzes/results.html', {})

# ***** this should probably go in a helper class
def pdfs(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    image = canvas.ImageReader('quizzes/BAGCA.jpg') # image_data is a raw string containing a JPEG

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawImage(image, 100, 600, 400, 200)
    p.drawString(250, 410, "Course Participant")
    p.drawString(215, 380, "has completed 10 hours of training.")
    #p.drawString(500, 825, "Hello world.")

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
def email(request, subject, message, from_addr, to_addr):
    #subject = 'Email subject'
    #message = 'Email message'
    #from_email = 'chas.barnajr@tsgforce.com'
    #to_email = 'chas.barnajr@tsgforce.com'
    if request.method == 'POST':
        list = []
        message = ''

        for value in request.POST:
            if 'question' in value:
                list.append(value)

        message = get_formatted_message(request.POST, list)

#        send_mail('Hello', message, 'chas.barnajr@tsgforce.com', ['sudhee1@gmail.com'], fail_silently=False)
        send_mail('Hello', message, 'chas.barnajr@tsgforce.com', [request.user.email], fail_silently=False)
        return HttpResponse(str(message))

    send_mail(subject, message, from_addr, to_addr, fail_silently=False)
    return
