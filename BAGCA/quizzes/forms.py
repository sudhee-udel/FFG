from django import forms


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.PasswordInput
    re_enter_password = forms.PasswordInput


class UploadQuizData(forms.Form):
    category_text = forms.CharField(label='Quiz name', max_length=200)
    category_description = forms.CharField(label='Quiz description', max_length=1000)
    course_code = forms.CharField(label='Course code', max_length=40)
    due_date = forms.DateField(label='Due date', widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    duration_hours = forms.DecimalField(label='Duration')
    required_score = forms.IntegerField(label='required_score')
    file = forms.Field(widget=forms.FileInput, label='Quiz file')
