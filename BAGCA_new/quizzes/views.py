from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.core.mail import send_mail
from quizzes.models import Question, Choice
from quiz_admin.models import Categories, Videos
from user_data.models import Completed
import random
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

    context = {'trainings': trainings_need_to_be_completed}
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

    context = {'training_info': training_info}
    return render(request, 'trainings/training.html', context)

@login_required
def quiz(request, training_id):
    if request.method == 'GET':
        try:
            latest_question_list = Question.objects.filter(category=training_id)
        except Question.DoesNotExist:
            raise Http404

        question_dictionary = {}
        for q in latest_question_list:
            question_dictionary[q] = sorted(q.choice_set.all(), key=lambda random_key: random.random())

        return render(request, 'trainings/quiz.html', {'question_dictionary': question_dictionary, 'training_id': training_id})

def process_results(request, training_id):
    if request.method == 'POST':
        question_list = []
        for value in request.POST:
            if 'question' in value:
                question_list.append(value)

        result_msg, correct, count = get_formatted_message(request.POST, question_list)

        score = int((float(correct)/float(count)) * 100)
        category = Categories.objects.get(pk=training_id)
        required_score = category.required_score

        if score >= category.required_score:
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

        context = {'result': result, 'required_score': required_score, 'result_msg': result_msg, 'correct': correct, 'count': count, 'score': score, 'color': color, 'training_id': training_id}

        return render(request, 'trainings/results.html', context)

@login_required
def results(request, training_id):
    return render(request, 'quizzes/results.html', {})

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

def email(request, subject, message):
    send_mail(subject, message, 'chas.barnajr@tsgforce.com', [request.user.email], fail_silently=False)
