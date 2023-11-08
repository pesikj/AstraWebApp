from django import forms


class UploadFileForm(forms.Form):
    file_field = forms.FileField()
    password = forms.CharField()

