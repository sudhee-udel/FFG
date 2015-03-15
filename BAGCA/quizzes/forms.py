from django import forms
from django.contrib.auth.models import Group


class UploadQuizData(forms.Form):
    group_choices = forms.ModelChoiceField(label="Assign quiz to group: ",
                                           queryset=Group.objects.all().order_by('name'))
    quiz_name = forms.CharField(label='Quiz name', max_length=200)
    quiz_description = forms.CharField(label='Quiz description', max_length=1000)
    trainer = forms.CharField(label='Trainer', max_length=100)
    course_code = forms.CharField(label='Course code', max_length=40)
    due_date = forms.DateField(label='Due date', widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    duration_hours = forms.DecimalField(label='Duration')
    required_score = forms.IntegerField(label='required_score')
    file = forms.Field(widget=forms.FileInput, label='Quiz file')