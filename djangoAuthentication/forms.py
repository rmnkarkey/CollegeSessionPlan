from django import forms

class UserForm(forms.Form):
    username=forms.CharField(max_length=299)
    password=forms.CharField(max_length=299)