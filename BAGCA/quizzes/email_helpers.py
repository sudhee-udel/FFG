from quizzes.models import Choice
from django.core.mail import send_mail
from quiz_admin.models import Categories

def email(request, subject, message):
    send_mail(subject, message, 'chas.barnajr@tsgforce.com', [request.user.email], fail_silently=False)

def send_success_email(request, training_id):
    # Send the mail to users, if they have passed the quiz
    current_quiz = Categories.objects.get(pk=training_id)
    subject = "You have finished the " + current_quiz.category_text + " quiz."
    message = "You have passed!\n\nPlease retain this message for your records."
    email(request, subject, message)

def get_formatted_message(post_data, question_list):
    count = 0
    correct = 0

    for item in sorted(question_list):
        count += 1
        choice_value = Choice.objects.get(pk=post_data.get(item, ''))

        if choice_value.answer:
            correct += 1

    return correct, count