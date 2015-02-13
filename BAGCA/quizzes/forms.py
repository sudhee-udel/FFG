from django import forms

class UploadQuizData(forms.Form):
    file = forms.Field(widget=forms.FileInput)