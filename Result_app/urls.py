from django.urls import path
from django.contrib import admin as ads
from .views import *

urlpatterns = [
    path('home_page/', index, name='index'),
    path('loop/', Result),
    path('session_result_view/', session_result_view, name='session_result_view'),
    path('student_list/', semester_result_list, name='semester_result_list'),
    path('session_result_list/', session_result_list, name='session_result_list'),
    # path('export_students_pdf/', export_students_pdf, name='export_students_pdf'),
    path('export_students_excel/', export_students_excel, name='export_students_excel'),
    path('export_students_csv/', export_students_csv, name='export_students_csv'),
    path('grade_export_students_excel/', grade_export_students_excel, name='grade_export_students_excel'),
    path('grade_export_students_csv/', grade_export_students_csv, name='grade_export_students_csv'),
    path('user_signup/', signup_function, name='signup'),
    path('', signin_function, name='signin'),
    path('user_signout/', user_signout, name='signout'),
]