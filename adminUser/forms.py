from django import forms
from .models import UserCredentials, AddResult

class UserCredentialsForm(forms.ModelForm):
    class Meta:
        model = UserCredentials
        fields = ['application_idU', 'first_name', 'last_name', 'middle_name', 'course_applied', 'password']

class AddResultForm(forms.ModelForm):
    class Meta:
        model = AddResult
        fields = ['application_idR','verbal_Comprehension', 'verbal_Reasoning', 'figural_Reasoning', 'qualitative_Reasoning', 'status']