from django import forms
from .models import Classroom,Student
from django.contrib.auth.models import User


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = '__all__'
        exclude =['teacher']

class Signup(forms.ModelForm):
    class Meta:
        model=User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets = {
        'password': forms.PasswordInput(),
        }

class Signin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())



class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude =['classroom']