### Step 1: Define Your Models
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)  # Assuming grades are like A, B, C, etc.

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade}"

### Step 2: Create Forms
from django import forms
from .models import Student, Result, Subject

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name']

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['subject', 'grade']

    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    grade = forms.ChoiceField(choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F')
    ])

### Step 3: Create the Views
from django.shortcuts import render, redirect
from .forms import StudentForm, ResultForm
from .models import Student, Result

def add_student_results(request):
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student = student_form.save()
            subjects = request.POST.getlist('subject')
            grades = request.POST.getlist('grade')
            for subject_id, grade in zip(subjects, grades):
                Result.objects.create(student=student, subject_id=subject_id, grade=grade)
            return redirect('student_list')  # Change this to the appropriate redirect target
    else:
        student_form = StudentForm()
        result_form = ResultForm()

    return render(request, 'add_student_results.html', {
        'student_form': student_form,
        'result_form': result_form,
        'subjects': Subject.objects.all()
    })

from django.urls import path
from .views import add_student_results

urlpatterns = [
    path('add_student_results/', add_student_results, name='add_student_results'),
]

### Step 1: Define Your Models
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)  # Assuming grades are like A, B, C, etc.

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade}"

### Step 2: Create Forms
from django import forms
from .models import Student, Result, Subject

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name']

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['subject', 'grade']

    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    grade = forms.ChoiceField(choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F')
    ])

### Step 3: Create the Views
from django.shortcuts import render, redirect
from .forms import StudentForm, ResultForm
from .models import Student, Result

def add_student_results(request):
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student = student_form.save()
            subjects = request.POST.getlist('subject')
            grades = request.POST.getlist('grade')
            for subject_id, grade in zip(subjects, grades):
                Result.objects.create(student=student, subject_id=subject_id, grade=grade)
            return redirect('student_list')  # Change this to the appropriate redirect target
    else:
        student_form = StudentForm()
        result_form = ResultForm()

    return render(request, 'add_student_results.html', {
        'student_form': student_form,
        'result_form': result_form,
        'subjects': Subject.objects.all()
    })

from django.urls import path
from .views import add_student_results

urlpatterns = [
    path('add_student_results/', add_student_results, name='add_student_results'),
    # other paths
]
