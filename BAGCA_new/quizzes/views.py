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
    if request.method == 'POST':
        list = []
        message = ''

        for value in request.POST:
            if 'question' in value:
                list.append(value)

         #message = message + "question_1 = " + request.POST.get('question_1', '') + "\n"

        message = get_formatted_message(request.POST, list)

#        send_mail('Hello', message, 'chas.barnajr@tsgforce.com', ['sudhee1@gmail.com'], fail_silently=False)
        send_mail('Hello', message, 'chas.barnajr@tsgforce.com', [request.user.email], fail_silently=False)


        return HttpResponse(str(message))
    latest_question_list = Question.objects.order_by('question_text')[:]
    question_dictionary = {}
    for q in latest_question_list:
        question_dictionary[q] = q.choice_set.all()

    category = {}
    category['url'] = Categories.objects.get(pk=Categories._get_pk_val(latest_question_list[0].category)).url

    context = {'question_dictionary': question_dictionary, 'category': category}
    return render(request, 'quizzes/index.html', context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404

    return render(request, 'quizzes/detail.html', {'question': question})

def vote(request, question_id):
    #return HttpResponse("You're voting on question %s." % question_id)
    latest_question_list = Question.objects.order_by('question_text')[:]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'quizzes/index.html', context)

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

def get_formatted_message(post_data, list):
    message = ''

    for item in sorted(list):
        question_re = re.match(r'question_(.*)', item, re.M)
        choice_value = Choice.objects.get(pk=post_data.get(item, ''))
        choice_result = ' wrong.'
        if choice_value.answer:
            choice_result = ' correct.'
        message = message + "For question: " + str(Question.objects.get(pk=question_re.groups(1)[0])) + " you chose: " + str(choice_value) + ". It is " + choice_result + "\n"


    return message

def email(subject, message, from_addr, to_addr):
    #subject = 'Email subject'
    #message = 'Email message'
    #from_email = 'chas.barnajr@tsgforce.com'
    #to_email = 'chas.barnajr@tsgforce.com'

    send_mail(subject, message, from_addr, to_addr, fail_silently=False)

    return


def training(request):
    return render(request, 'quizzes/test.html', {})
