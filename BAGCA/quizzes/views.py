from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from quiz_admin.models import Quiz
from .models import Question
from user_data.models import Completed, UserAssignment
from .helpers import get_result_page_styling, save_user_completion, get_questions_for_quiz, save_user_assignment, \
    get_admin_assigned_trainings, get_current_quiz, get_quizzes_needed_to_be_completed, \
    get_users_groups_need_to_complete_quizzes, get_training_page_content, get_remaining_trainings
from .email_helpers import get_formatted_message
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def check_user_status(request):
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

    quizzes = []

    for quiz_needed_to_be_finished in quizzes_needed_to_be_completed:
        quizzes.append(quiz_needed_to_be_finished)

    paginated_user_mail = Paginator(quizzes, 5)
    page = request.GET.get('page')
    paginated_user_mail_list = {}
    try:
        paginated_user_mail_list['user_list'] = paginated_user_mail.page(page)
    except PageNotAnInteger:
        paginated_user_mail_list['user_list'] = paginated_user_mail.page(1)
    except EmptyPage:
        paginated_user_mail_list['user_list'] = paginated_user_mail.page(paginated_user_mail.num_pages)

    if paginated_user_mail.num_pages > 1:
        paginate = True
    else:
        paginate = False


    context = {'paginated_user_mail_list': paginated_user_mail_list, 'users': users, 'groups': groups,
               'quizzes': quizzes, 'paginate': paginate}
    return render(request, "check_user_status.html", context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {
        'form': form,
    })


@login_required
def index(request):
    if request.user.groups.all():
        trainings_needed_to_be_completed, user_assigned = get_remaining_trainings(request)

        training_groups = {}

        for remaining_trainings in trainings_needed_to_be_completed:
            for group in remaining_trainings.groups.all():
                number_of_trainings_in_group = training_groups.get(group, 0)
                training_groups[group] = number_of_trainings_in_group + 1

        context = {'training_groups': training_groups, 'user_assigned': user_assigned}
    elif request.user.first_name == '' or request.user.last_name == '' or request.user.email == '':
        return render(request, 'profile.html')
    else:
        groups = Group.objects.all()
        context = {'no_groups': True, 'groups': groups}

    return render(request, 'index.html', context)


@login_required
def show_course_trainings(request, group_id):
    trainings_needed_to_be_completed, user_assigned = get_remaining_trainings(request)

    filtered_trainings = set()

    for training in trainings_needed_to_be_completed:
        for current_group in training.groups.all():
            if int(current_group.id) == int(group_id):
                filtered_trainings.add(training)

    context = {'trainings': filtered_trainings}

    return render(request, 'course_training.html', context)


@login_required
def print_past_certificates(request):
    completed_trainings = Completed.objects.filter(user=request.user)

    completed_training_list = []

    for training in completed_trainings:
        data = {'quiz_name': training.quiz, 'date_completed': training.date_completed}

        completed_training_list.append(data)

    context = {'trainings': completed_training_list}

    return render(request, 'print_past_certificates.html', context)


@login_required
def trainings(request):
    alert_msg = ""
    alert_style = ""

    if request.method == 'POST':
        training_id = request.POST['training_id']
        result = save_user_assignment(request, training_id)

        if result == "added":
            alert_msg = "You have successfully assigned a training to yourself!"
            alert_style = "alert-success"
        elif result == "exists":
            alert_msg = "You have already assigned this training to yourself."
            alert_style = "alert-info"
        else:
            alert_msg = "An error has occurred when trying to assign training. Please report this to an administrator."
            alert_style = "alert-danger"

    admin_assigned_trainings = get_admin_assigned_trainings(request)
    available_trainings = Quiz.objects.all()

    available_trainings_users_can_add = set()

    # Add all available trainings
    for available_training in available_trainings:
        available_trainings_users_can_add.add(available_training)

    trainings_assigned_by_user = UserAssignment.objects.filter(user=request.user)
    already_assigned = set()

    # Remove the trainings already assigned to the user by the admin
    for assigned_trainings in trainings_assigned_by_user:
        already_assigned.add(assigned_trainings.quiz)

    completed_trainings = Completed.objects.filter(user=request.user)
    completed_training_ids = set()

    # Remove the trainings that the user has already completed
    for completed in completed_trainings:
        completed_training_ids.add(completed.quiz)

    available_trainings_users_can_add = available_trainings_users_can_add.difference(admin_assigned_trainings)
    available_trainings_users_can_add = available_trainings_users_can_add.difference(already_assigned)
    available_trainings_users_can_add = available_trainings_users_can_add.difference(completed_training_ids)

    context = {'trainings': available_trainings_users_can_add, 'alert_msg': alert_msg, 'alert_style': alert_style}
    return render(request, 'trainings.html', context)


@login_required
def remove_user_assignment(request, training_id):
    assignment = UserAssignment.objects.get(quiz_id=training_id, user_id=request.user.id)
    assignment.delete()
    return redirect("/")


@login_required
def profile(request):
    if request.method == 'GET':
        context = {'groups': request.user.groups.all()}
        return render(request, 'profile.html', context)

    elif request.method == 'POST':
        existing_user = User.objects.filter(email=request.POST['email'])
        if (len(existing_user) == 0) or (len(existing_user) > 0 and str(existing_user[0].username) == str(request.user)):
            user = request.user
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
        elif str(existing_user[0].username) != str(request.user):
            context = {'groups': request.user.groups.all(), 'email_error':  True}
            return render(request, 'profile.html', context)

        return redirect("/")


@login_required
def user_assigned_training(request, training_id):
    context = get_training_page_content(request, training_id)

    return render(request, 'trainings/training.html', context)


@login_required
def quiz(request, training_id):
    question_dictionary = get_questions_for_quiz(training_id)

    context = {'question_dictionary': question_dictionary, 'training_id': training_id}

    return render(request, 'trainings/quiz.html', context)


@login_required
def quiz_incomplete(request, training_id):
    question_dictionary = get_questions_for_quiz(training_id)

    context = {'question_dictionary': question_dictionary, 'training_id': training_id, 'incomplete': True}

    return render(request, 'trainings/quiz.html', context)


def process_results(request, training_id):
    if request.method == 'POST':
        question_list = []
        for value in request.POST:
            if 'question' in value:
                question_list.append(value)

        questions = Question.objects.filter(quiz=training_id)

        if len(questions) != len(question_list):
            return quiz_incomplete(request, training_id)

        correct_answers, total_number_of_questions = get_formatted_message(request.POST, question_list)

        current_quiz = get_current_quiz(training_id)

        required_score = current_quiz.required_score

        result, color, score = get_result_page_styling(correct_answers, total_number_of_questions, required_score)

        if result == 'passed':
            check_if_user_assigned_quiz = UserAssignment.objects.filter(quiz=training_id, user=request.user)

            if check_if_user_assigned_quiz:
                check_if_user_assigned_quiz.delete()

            save_user_completion(request, training_id)

        context = {'result': result, 'required_score': required_score, 'correct': correct_answers,
                   'count': total_number_of_questions, 'score': score, 'color': color, 'training_id': training_id}

        return render(request, 'trainings/results.html', context)


def access_past_trainings(request, training_id):
    context = get_training_page_content(request, training_id)

    return render(request, 'trainings/view_training_material.html', context)
