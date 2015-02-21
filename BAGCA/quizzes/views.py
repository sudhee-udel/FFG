from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from quiz_admin.models import Categories, Videos, Files
from user_data.models import Completed, UserAssignment
from .helpers import get_result_page_styling, save_user_completion, get_questions_for_quiz, save_user_assignment, \
    get_admin_assigned_trainings, get_user_assigned_trainings, get_current_quiz
from .email_helpers import get_formatted_message
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def index(request):
    trainings_need_to_be_completed = get_admin_assigned_trainings(request)

    user_assigned = get_user_assigned_trainings(request)

    # Subtract any trainings that are assigned to the user
    if len(trainings_need_to_be_completed) != 0:
        user_assigned = user_assigned.difference(trainings_need_to_be_completed)

    context = {'trainings': trainings_need_to_be_completed, 'user_assigned': user_assigned}
    return render(request, 'index.html', context)

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
    available_trainings = Categories.objects.all()

    available_trainings_users_can_add = set()

    # Add all available trainings
    for available_training in available_trainings:
        available_trainings_users_can_add.add(available_training)

    trainings_assigned_by_user = UserAssignment.objects.filter(user=request.user)
    already_assigned = set()

    # Remove the trainings already assigned to the user by the admin
    for assigned_trainings in trainings_assigned_by_user:
        already_assigned.add(assigned_trainings.category)

    completed_trainings = Completed.objects.filter(user=request.user.email)
    completed_training_ids = set()

    # Remove the trainings that the user has already completed
    for completed in completed_trainings:
        completed_training_ids.add(completed.category)

    available_trainings_users_can_add = available_trainings_users_can_add.difference(admin_assigned_trainings)
    available_trainings_users_can_add = available_trainings_users_can_add.difference(already_assigned)
    available_trainings_users_can_add = available_trainings_users_can_add.difference(completed_training_ids)

    context = {'trainings': available_trainings_users_can_add, 'alert_msg': alert_msg, 'alert_style': alert_style}
    return render(request, 'trainings.html', context)

@login_required
def remove_user_assignment(request, training_id):
    assignment = UserAssignment.objects.get(category_id=training_id, user_id=request.user.id)
    assignment.delete()
    return redirect("/")

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

    paginated_videos = Paginator(video_list, 1)
    page = request.GET.get('page')

    try:
        training_info['videos'] = paginated_videos.page(page)
    except PageNotAnInteger:
        training_info['videos'] = paginated_videos.page(1)
    except EmptyPage:
        training_info['videos'] = paginated_videos.page(paginated_videos.num_pages)

    training_info['title']= category.category_text
    training_info['description'] = category.category_description
    training_info['id'] = training_id

    if paginated_videos.num_pages > 1:
        paginate = True
    else:
        paginate = False

    quiz_files = Files.objects.filter(category_id=training_id)

    context = {'training_info': training_info, 'paginate': paginate, 'files': quiz_files}
    return render(request, 'trainings/training.html', context)

@login_required
def quiz(request, training_id):
    question_dictionary = get_questions_for_quiz(training_id)

    return render(request, 'trainings/quiz.html', {'question_dictionary': question_dictionary, 'training_id': training_id})

def process_results(request, training_id):
    if request.method == 'POST':
        question_list = []
        for value in request.POST:
            if 'question' in value:
                question_list.append(value)

        correct_answers, total_number_of_questions = get_formatted_message(request.POST, question_list)

        current_quiz = get_current_quiz(training_id)

        required_score = current_quiz.required_score

        result, color, score = get_result_page_styling(correct_answers, total_number_of_questions, required_score)

        if result == 'passed':
            check_if_user_assigned_quiz = UserAssignment.objects.filter(category=training_id, user=request.user)

            if check_if_user_assigned_quiz:
                check_if_user_assigned_quiz.delete()

            save_user_completion(request, training_id)

        context = {'result': result, 'required_score': required_score, 'correct': correct_answers,
                   'count': total_number_of_questions, 'score': score, 'color': color, 'training_id': training_id}

        return render(request, 'trainings/results.html', context)

@login_required
def results(request):
    return render(request, 'quizzes/results.html', {})
