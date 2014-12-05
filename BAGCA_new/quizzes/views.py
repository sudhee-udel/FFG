import time

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from quizzes.models import Question, Choice
import re

def index(request):
    if request.method == 'POST':
        list = []
        message = ''
        for value in request.POST:
            if 'question' in value:
                list.append(value)

         #message = message + "question_1 = " + request.POST.get('question_1', '') + "\n"

        message = get_formatted_message(request.POST, list)

        send_mail('Hello', message, 'chas.barnajr@tsgforce.com', ['sudhee1@gmail.com'], fail_silently=False)

        return HttpResponse(str(message))
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    question_dictionary = {}
    for q in latest_question_list:
        question_dictionary[q] = q.choice_set.all()

    context = {'question_dictionary': question_dictionary}
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

def results(request):
    return HttpResponse("Hello.")

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
