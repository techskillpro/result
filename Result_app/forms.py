from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


# CLASS FOR USER SIGNUP
class UserCreation(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Your Username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Enter Your Email Address'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


class StudentForm(forms.ModelForm):
    try:
        plans = Department.objects.all()
        plan_list = []
        for plan in plans:
            plan_sample = (plan.id, plan.name)
            plan_list.append(plan_sample)
    except:
        plan_list=[]
    
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    level = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    registration_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    session = forms.ModelChoiceField(queryset=Session.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = '__all__'


class ResultForm(forms.ModelForm):
    class Meta:
        model = Semester_Result
        fields = [
            'course',
            # 'semester',
            # 'session',
            'total_mark'
        ]

    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    total_mark = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control'}))


class SessionResultForm(forms.ModelForm):
    class Meta:
        model = Session_Result
        fields = [
            'student',
            'session',
            'semesteresult1',
            'semesteresult2',
        ]

    student = forms.ModelChoiceField(queryset=Student.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    session = forms.ModelChoiceField(queryset=Session.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    semesteresult1 = forms.ModelChoiceField(queryset=Semester_Result.objects.filter(semester=1), widget=forms.Select(attrs={'class':'form-control'}))
    semesteresult2 = forms.ModelChoiceField(queryset=Semester_Result.objects.filter(semester=2), widget=forms.Select(attrs={'class':'form-control'}))
