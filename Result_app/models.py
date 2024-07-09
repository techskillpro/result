from django.db import models


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=500, null=False, blank=False)
    level = models.CharField(max_length=500, null=False, blank=False)
    registration_number = models.CharField(max_length=500, null=False, blank=False)
    # department = models.CharField(max_length=500, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.DO_NOTHING, max_length=500, null=True, blank=True)
    
    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=500, null=False, blank=False)
    level = models.CharField(max_length=500, null=False, blank=False)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    department = models.ForeignKey(Department,  null=True, blank=True, on_delete=models.DO_NOTHING)
    semester = models.ForeignKey('Semester',  null=True, blank=True, on_delete=models.DO_NOTHING)
    session = models.CharField(max_length=200, null=True, blank=True)
    course_code = models.CharField(max_length=500, null=False, blank=False)
    credit = models.IntegerField(null=True, blank=True)
    level = models.CharField(max_length=500, null=False, blank=False)

    def __str__(self):
        return self.course_code


class Session(models.Model):
    name = models.CharField(max_length=500, null=False, blank=False)

    def __str__(self):
        return self.name


class Semester(models.Model):
    choice_list=[
        ('FIRST SEMESTER', 'FIRST SEMESTER'),
        ('SECOND SEMESTER', 'SECOND SEMESTER'),
    ]
    name = models.CharField(choices=choice_list, max_length=500, null=False, blank=False)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.name


class Course_Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    semester = models.ForeignKey(Semester, on_delete=models.DO_NOTHING)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    score = models.FloatField(null=True, blank=True)
    grade_point = models.IntegerField(null=True, blank=True)
    total_point = models.IntegerField(null=True, blank=True)
    letter_grade = models.CharField(max_length=200, null=True, blank=True)
    level = models.CharField(max_length=200, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.DO_NOTHING, max_length=500, null=True, blank=True)
    semester_result = models.ForeignKey('Semester_Result', on_delete=models.DO_NOTHING, max_length=200, null=True, blank=True)


    def __str__(self):
        return f'{self.student.name} {self.course} result for {self.semester} semester'
    

class Semester_Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    # course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    semester = models.ForeignKey(Semester, on_delete=models.DO_NOTHING)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    gpa = models.FloatField(blank=True, null=True)
    remark = models.CharField(max_length=200, null=True, blank=True)
    level = models.CharField(max_length=200, null=True, blank=True)
    # department = models.CharField(max_length=200, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.DO_NOTHING, max_length=500, null=True, blank=True)

    def save(self, force_insert=False, *args, **kwargs):
        if 1.00 > float(self.gpa) >= 0:
            self.remark = 'FAIL'

        elif 1.50 > float(self.gpa) >= 1.00:
            self.remark = 'LOWER PASS'

        elif  2.40> float(self.gpa) >= 1.50:
            self.remark = 'PASS'

        elif 3.50 > float(self.gpa) >= 2.40:
            self.remark = 'MERIT'

        elif 4.50 > float(self.gpa) >= 3.50:
            self.remark = 'CREDIT'

        elif 5.00 >= float(self.gpa) >= 4.50:
            self.remark = 'DISTINCTION'

        self.gpa = round(self.gpa, 2)
        super().save(force_insert=force_insert, *args, **kwargs)

    def __str__(self):
        return f'{self.student.name} {self.semester} result for {self.session} session. GPA-[{self.gpa}]'

    
class Session_Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    semesteresult1 = models.ForeignKey(Semester_Result, related_name='first_semester_Result', on_delete=models.DO_NOTHING)
    semesteresult2 = models.ForeignKey(Semester_Result, related_name='second_semester_result', on_delete=models.DO_NOTHING)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    cgpa = models.FloatField(blank=True, null=True)
    remark = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.student.name} result for {self.session} session. CGPA-[{self.cgpa}]'


    
        self.gpa = round(self.gpa, 2)

    def save(self, *args, **kwargs):
        self.cgpa = round(self.cgpa, 2)
        super().save(*args, **kwargs)
        