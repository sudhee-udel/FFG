import re
from quizzes.models import Choice, Question
from django.core.mail import send_mail
from quiz_admin.models import Categories
from quizzes.helpers import save_user_completion

def email(request, subject, message):
    send_mail(subject, message, 'chas.barnajr@tsgforce.com', [request.user.email], fail_silently=False)

def send_success_email(request, training_id):
    save_user_completion(request, training_id)

    # Send the mail to users, if they have passed the quiz
    current_quiz = Categories.objects.get(pk=training_id)
    subject = "You have finished the " + current_quiz.category_text + " quiz."
    message = "You have passed!\n\nPlease retain this message for your records."
    email(request, subject, message)

def get_formatted_message(post_data, question_list):
    message = []
    count = 0
    correct = 0

    for item in sorted(question_list):
        count += 1
        question_re = re.match(r'question_(.*)', item, re.M)
        choice_value = Choice.objects.get(pk=post_data.get(item, ''))
        choice_result = 'wrong.'
        if choice_value.answer:
            correct += 1
            choice_result = 'correct.'
        message.append("For question: " + str(Question.objects.get(pk=question_re.groups(1)[0])) + " You chose: " + str(choice_value) + ". It is " + choice_result + "\n")

    return message, correct, count