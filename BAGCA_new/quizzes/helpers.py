from quiz_admin.models import Categories
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse
from quizzes.email_helpers import send_success_email

def determine_pass_or_fail(correct_answers, total_number_of_questions, required_score):
    score = int((float(correct_answers)/total_number_of_questions) * 100)

    if score >= required_score:
        return True, score
    else:
        return False, score

def get_result_page_styling(result_package):
    result, score = determine_pass_or_fail(result_package['correct_answers'], result_package['total_number_of_questions'], result_package['required_score'])
    if result:
        send_success_email(result_package['request'], result_package['training_id'])
        return "passed", "green", score
    else:
        return "failed", "red", score

def set_certificate_properties(pdf):
    image = canvas.ImageReader('quizzes/BAGCA.jpg') # image_data is a raw string containing a JPEG

    pdf.drawImage(image, 100, 600, 400, 200)
    pdf.setLineWidth(.5)

    # Add the outer borders; vertical lines
    pdf.line(10,830,10,10)
    pdf.line(585,830,585,10)

    # Add the inner borders; vertical lines
    pdf.line(15,825,15,15)
    pdf.line(580,825,580,15)

    # Add the outer borders; horizontal lines
    pdf.line(10,10,585,10)
    pdf.line(10,830,585,830)

    # Add the inner borders; horizontal lines
    pdf.line(15,15,580,15)
    pdf.line(15,825,580,825)

    return pdf

def generate_certificate(request, training_id):
    category = Categories.objects.get(pk=training_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate_of_completion.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    pdf = canvas.Canvas(buffer)

    pdf.setFont('Helvetica', 30)

    user_first_last_name = request.user.first_name + " " + request.user.last_name

    if user_first_last_name.strip() == '':
        user_first_last_name = request.user.email.split("@")[0]

    user_name_length = len(user_first_last_name)/2
    pdf.drawString(250 - user_name_length, 410, user_first_last_name)
    pdf.setFont('Helvetica', 20)

    message = "has completed " + str(category.duration_hours) + " hours of training."

    pdf.drawString(175 - len(message)/2, 380, message)

    set_certificate_properties(pdf)

    # Close the PDF object cleanly.
    pdf.showPage()
    pdf.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response