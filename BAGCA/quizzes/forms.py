from django import forms

class UploadQuizData(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()