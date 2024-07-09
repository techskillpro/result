from django.shortcuts import render, redirect
from django.http import HttpResponse,  HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import forms
from . import models
from .utils import GPA_ENGINE, grade_eng
from django.contrib.auth.decorators import login_required
import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import csv

# Create your views here.


@login_required(login_url='signin')
def index(request):
    return render(request, 'base.html')


def signup_function(request):
    form = forms.UserCreation()
    if request.method == 'POST':
        form = forms.UserCreation(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Successfully created')
            return redirect('signin')

    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)


def signin_function(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'You have logged in successfully!')
            return redirect('index')
        else:
            messages.error(request, 'Failed to Login User!')
    return render(request, 'signin.html')


@login_required(login_url='signin')
def user_signout(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def index(request):
    if request.method == 'POST':
        student_form = forms.StudentForm(request.POST)
        
        # To check 
        name = request.POST.get('name')
        session=request.POST.get('session')
        semester=request.POST.get('semester')
        level=request.POST.get('level')
        department=request.POST.get('department')
        total_mark=request.POST.getlist('total_mark')
        course = request.POST.getlist('course')

        stud = models.Student.objects.filter(name=name).exists()
        
        if stud:
            student = models.Student.objects.get(name=name)
            # print(student)
        else:
            if student_form.is_valid():
                student = student_form.save()


        course_list=[]
    
        for course_id, total_mark_id in zip(course, total_mark):
            grade = grade_eng(total_mark_id)
            # print(grade[0])
            courser=models.Course.objects.get(id=course_id)
            courses = models.Course_Result.objects.create(
                student=student,
                course=courser,
                semester=models.Semester.objects.get(id=semester),
                session=models.Session.objects.get(id=session),
                score=int(total_mark_id),
                department=models.Department.objects.get(id=department),
                total_point=int(grade[1]) * int(courser.credit),
                letter_grade=grade[0],
                level=level,
            )
            course_list.append(courses)

        gpa = GPA_ENGINE(course_list)

        sems = models.Semester_Result(
            student=student,
            semester=models.Semester.objects.get(id=semester),
            session=models.Session.objects.get(id=session),
            gpa=gpa,
            level=request.POST.get('level'),
            department=models.Department.objects.get(id=department),
        )
        sems.save(force_insert=False)

        for result in course_list:
            result.semester_result = sems
            courses.save()

        messages.success(request, f'Result Successfully Calculated and Saved. GPA = {gpa}')
        return redirect('index')
    else:
        student_form = forms.StudentForm()
        result_form = forms.ResultForm()

    result_form = forms.ResultForm()
    return render(request, 'index.html', {
        'student_form': student_form,
        'result_form': result_form,
        'subjects': models.Course.objects.all()
    })


@login_required(login_url='signin')
def session_result_view(request):
    form = forms.SessionResultForm()
    if request.method == 'POST':
        form = forms.SessionResultForm(request.POST)
        if form.is_valid():
            save_form = form.save()
            semes1 = models.Semester_Result.objects.get(id=request.POST.get('semesteresult1'))
            semes2 = models.Semester_Result.objects.get(id=request.POST.get('semesteresult2'))
            sum_gp = float(semes1.gpa) + float(semes2.gpa)
            cgpa = float(sum_gp)/2
            # print(cgpa)

            if 1.00 > float(cgpa) >= 0:
                save_form.remark = 'FAIL'

            elif 1.50 > float(cgpa) >= 1.00:
                save_form.remark = 'LOWER PASS'

            elif 2.40 > float(cgpa) >= 1.50:
                save_form.remark = 'PASS'

            elif 3.50 > float(cgpa) >= 2.40:
                save_form.remark = 'MERIT'

            elif 4.50 > float(cgpa) >= 3.50:
                save_form.remark = 'CREDIT'

            elif 5.00 >= float(cgpa) >= 4.50:
                save_form.remark = 'DISTINCTION'

            save_form.cgpa = cgpa
            # print(save_form.remark)
            save_form.save()
            messages.success(request, f'Result Successfully Calculated and Saved. CGPA = {cgpa}')
            return redirect('session_result_view')
    return render(request, 'index1.html', {'forms': form})


@login_required(login_url='signin')
def semester_result_list(request):
    query = request.GET.get('q')
    query2 = request.GET.get('r')
    query3 = request.GET.get('s')
    query4 = request.GET.get('t')
    if query:
        lister = {
            'level' : query,
            'department' : query2,
            'semester' : query3,
            'session' : query4,
        }
        z = request.session['lister'] = lister
        students = models.Semester_Result.objects.filter(level__icontains=query, department__name__icontains=query2, semester__name__icontains=query3, session__name__icontains=query4)

    else:
        students = models.Semester_Result.objects.all()
    # print(query2)
    # print(query3)
    # print(query4)
    # print(students)

    return render(request, 'grade.html', {'students': students})


def Result(request):
    courses = models.Course_Result.objects.filter(
        student__name__icontains='OLAOYE ABDULRASHEED OYEYEMI',
        semester__name__icontains='FIRST SEMESTER',
        session__name__icontains='2020/2021',
    )
    # print(courses)
    
    for course in courses:
        course.semester_result = models.Semester_Result.objects.get(
            id=46,
        # uuu = models.Semester_Result.objects.filter(
            # student__name__icontains='AKANGBE MORADEYO SHERIFAT',
            # semester__name__icontains='FIRST SEMESTER',
            # session__name__icontains='2020/2021',
        )
    # print(uuu)
    # print(models.Semester_Result.objects.filter(education=0))
    
        course.save()
                                                                                    
    return HttpResponse('all good')


@login_required(login_url='signin')
def grade_export_students_excel(request):
    # Fetch all student records
    abc=request.session.get('lister')
    students = models.Semester_Result.objects.filter(level__icontains=abc['level'], department__name__icontains=abc['department'], semester__name__icontains=abc['semester'], session__name__icontains=abc['session'])
    courses = models.Course.objects.filter(level__icontains=abc['level'], department__name__icontains=abc['department'], semester__name__icontains=abc['semester'])
    # course__results = models.Course_Result.objects.filter(level__icontains=abc['level'], department__name__icontains=abc['department'], semester__name__icontains=abc['semester'])
    # course__resulter = models.Course_Result.objects.filter(level__icontains=abc['level'], department__name__icontains='GENERAL STUDIES', semester__name__icontains=abc['semester'])
    # print(course__results)
    # print(course__resulter)


    # return HttpResponse('Okay')

    # Create a new workbook and get the active worksheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = f"Semester Result"


    # # Write the header row
    lista = ['Student Name', 'Matric Number', 'Session', 'Semester', 'Level', 'Department', 'GPA', 'Remark']
    for course in courses:
        lista.append(course.course_code)
    # print(lista)
    sheet.append(lista)
    
    # Write the data rows
    for student in students:
        course__resultser = models.Course_Result.objects.filter(student__name__icontains=student.student.name, level__icontains=abc['level'], session__name__icontains=abc['session'], semester__name__icontains=abc['semester'])
        # print(abc['semester'])
        # print(abc['session'])
        # print(abc['level'])
        # print(student.student.name)
        # print(course__resultser)
        listb=[
            student.student.name,
            student.student.registration_number,
            student.session.name,
            student.semester.name,
            student.student.level,
            student.department.name,
            student.gpa,
            student.remark,
        ]
        for std in course__resultser:
                listb.append(f'{std.course.course_code}: {std.letter_grade}')
        sheet.append(listb)
    
    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Semester_Result.xlsx'

    # Save the workbook to the response
    workbook.save(response)
    del request.session['lister']

    return response


# def export_students_pdf(request):
#     abc=request.session.get('lister')
#     students = models.Semester_Result.objects.filter(level__icontains=abc['level'], department__icontains=abc['department'], semester__name__icontains=abc['semester'], session__name__icontains=abc['session'])
#
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="students_result.pdf"'
#
#     pdf = canvas.Canvas(response, pagesize=letter)
#     pdf.setTitle("Students Results")
#
#     pdf.drawString(100, 750, "Students List")
#     pdf.drawString(100, 730, "Name")
#     pdf.drawString(300, 730, "Class")
#     pdf.drawString(500, 730, "Level")
#
#     y = 710
#     for student in students:
#         pdf.drawString(100, y, student.name)
#         pdf.drawString(300, y, student.department)
#         pdf.drawString(500, y, student.level)
#         y -= 20
#
#     pdf.showPage()
#     pdf.save()
#     return response


@login_required(login_url='signin')
def grade_export_students_csv(request):
    abc=request.session.get('lister')
    students = models.Semester_Result.objects.filter(level__icontains=abc['level'], department__icontains=abc['department'], semester__name__icontains=abc['semester'], session__name__icontains=abc['session'])

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Matric NUmber', 'Session', 'Semester', 'Level', 'Department', 'GPA', 'Remark'])
    for student in students:
        writer.writerow([student.student.name, student.student.registration_number, student.session.name, student.semester.name, student.level,
                      student.department, student.gpa, student.remark])
    del request.session['lister']

    return response


@login_required(login_url='signin')
def session_result_list(request):
    query = request.GET.get('q')
    query2 = request.GET.get('r')
    query3 = request.GET.get('s')
    if query:
        lister = {
            'level' : query,
            'department' : query2,
            'session' : query3,
        }
        z = request.session['lister'] = lister
        students = models.Session_Result.objects.filter(student__level__icontains=query, student__department__icontains=query2, session__name__icontains=query3)
    else:
        students = models.Session_Result.objects.all()

    return render(request, 'session.html', {'students': students})


@login_required(login_url='signin')
def export_students_excel(request):
    # Fetch all student records
    abc=request.session.get('lister')
    students = models.Session_Result.objects.filter(student__level__icontains=abc['level'], student__department__icontains=abc['department'],
                                                     session__name__icontains=abc['session'])

    # Create a new workbook and get the active worksheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = f"Session Result"

    # Write the header row
    sheet.append(['Student Name', 'Matric Number', 'Session', 'Level', 'Department', 'First Semester GPA', 'Second Semester GPA', 'CGPA', 'Remark'])

    # Write the data rows
    for student in students:
        sheet.append([student.student.name, student.student.registration_number, student.session.name, student.student.level,
                      student.student.department, student.semesteresult1.gpa, student.semesteresult2.gpa, student.cgpa, student.remark])

    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Session_Result.xlsx'

    # Save the workbook to the response
    workbook.save(response)
    del request.session['lister']

    return response


@login_required(login_url='signin')
def export_students_csv(request):
    abc=request.session.get('lister')
    students = models.Session_Result.objects.filter(student__level__icontains=abc['level'], student__department__icontains=abc['department'],
                                                     session__name__icontains=abc['session'])

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="session_result.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Matric Number', 'Session', 'Level', 'Department', 'First Semester GPA', 'Second Semester GPA', 'CGPA', 'Remark'])
    for student in students:
        writer.writerow([student.student.name, student.student.registration_number, student.session.name, student.student.level,
                      student.student.department, student.semesteresult1.gpa, student.semesteresult2.gpa, student.cgpa, student.remark])
    del request.session['lister']
    return response