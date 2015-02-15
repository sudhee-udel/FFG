from django import forms


class UploadQuizData(forms.Form):
    category_text = forms.CharField(label='Quiz name', max_length=100)
    category_description = forms.CharField(label='Quiz description', max_length=1000)
    course_code = forms.CharField(label='Course code', max_length=100)
    due_date = forms.DateField(label='Due date')
    duration_hours = forms.IntegerField(label='Duration')
    required_score = forms.IntegerField(label='required_score')
    file = forms.Field(widget=forms.FileInput, label='File')
