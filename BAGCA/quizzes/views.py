from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from quiz_admin.models import Categories, Videos, Files
from user_data.models import Completed, UserAssignment
from .helpers import get_result_page_styling, save_user_completion, get_questions_for_quiz, save_user_assignment
from .email_helpers import get_formatted_message
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
        check_if_user_finished_quiz = Completed.objects.filter(category=quiz_id, user=request.user.email)
        quiz_name = Categories.objects.get(pk=quiz_id)
        if not check_if_user_finished_quiz:
            trainings_need_to_be_completed.add(quiz_name)

    user_assignments = UserAssignment.objects.filter(user=request.user)
    user_assigned = set()

    for assignment in user_assignments:
        user_assigned.add(assignment.category)

    print user_assigned

    context = {'trainings': trainings_need_to_be_completed, 'user_assigned': user_assigned}
    return render(request, 'index.html', context)

@login_required
def trainings(request):
    alert_msg = ""
    alert_style = ""

    if request.method == 'POST':
        user = request.user
        training_id = request.POST['training_id']
        result = save_user_assignment(request, training_id)

        if result=="added":
            alert_msg = "You have successfully assigned a training to yourself!"
            alert_style = "alert-success"
        elif result=="exists":
            alert_msg = "You have already assigned this training to yourself."
            alert_style = "alert-info"
        else:
            alert_msg = "An error has occurred when trying to assign training. Please report this to an administrator."
            alert_style = "alert-danger"

    trainings = Categories.objects.all()
    context = {'trainings': trainings, 'alert_msg': alert_msg, 'alert_style': alert_style }
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

        current_quiz = Categories.objects.get(pk=training_id)

        required_score = current_quiz.required_score

        result, color, score = get_result_page_styling(correct_answers, total_number_of_questions, required_score)

        if result == 'passed':
            save_user_completion(request, training_id)

        context = {'result': result, 'required_score': required_score, 'correct': correct_answers, 'count': total_number_of_questions, 'score': score, 'color': color, 'training_id': training_id}

        return render(request, 'trainings/results.html', context)

@login_required
def results(request):
    return render(request, 'quizzes/results.html', {})
