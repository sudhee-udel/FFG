from django import forms

class UploadQuizData(forms.Form):
    category_text = forms.CharField(label='Quiz name', max_length=200)
    category_description = forms.CharField(label='Quiz description', max_length=1000)
    trainer = forms.CharField(label='Trainer', max_length=100)
    course_code = forms.CharField(label='Course code', max_length=40)
    due_date = forms.DateField(label='Due date', widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    duration_hours = forms.DecimalField(label='Duration')
    required_score = forms.IntegerField(label='required_score')
    file = forms.Field(widget=forms.FileInput, label='Quiz file')
