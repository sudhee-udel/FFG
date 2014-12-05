import time

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail

from quizzes.models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'quizzes/index.html', context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404

    return render(request, 'quizzes/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of the question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    #return HttpResponse("You're voting on question %s." % question_id)
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'quizzes/index.html', context)

def email(request):
    subject = 'Test - You have successfully completed training!'
    message = "Test\r\n\r\nThis is your training certificate\r\nDate: " + time.strftime("%m/%d/%Y %H:%M %Z")
    from_email = 'chas.barnajr@tsgforce.com'
    to_email = request.POST.get('address_field') 
    
    send_mail(subject, message, from_email, [to_email], fail_silently=False)

    return HttpResponseRedirect('/quizzes/')
