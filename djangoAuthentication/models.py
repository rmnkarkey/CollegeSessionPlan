from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save

class CourseManagement(models.Model):
    course_code = models.CharField(max_length=50,primary_key=True)
    course_name = models.CharField(max_length=50)
    credit = models.IntegerField(max_length=1)
    prerequisite = models.CharField(max_length=299,default=None)

    def __str__(self):
        return self.course_name

class OfferedCourses(models.Model):
    id = models.IntegerField(primary_key=True)
    courseCode = models.ForeignKey(CourseManagement,on_delete=models.CASCADE)
    session = models.CharField(max_length=4)

class SessionNameTable(models.Model):
    session_name=models.CharField(primary_key=True,max_length=100)
    session_year = models.IntegerField(max_length=4)
    date_created=models.DateField(default=timezone.now().date())
    max_credit = models.IntegerField()
    start_date = models.DateField(default=timezone.now().date())
    end_date = models.DateField(default=timezone.now().date())

    class Meta:
        ordering=('-start_date',)

class SessionCourseTable(models.Model):
    session_name = models.ForeignKey(SessionNameTable,on_delete=models.CASCADE)
    session_session = models.CharField(max_length=100)
    courseCode = models.ForeignKey(CourseManagement,on_delete=models.CASCADE)
    course_credit = models.IntegerField(max_length=1)
    Offered=models.CharField(max_length=3)

class StudentManagement(models.Model):
    student_id = models.ForeignKey(User,on_delete=models.CASCADE)
    university_id = models.IntegerField(primary_key=True)
    full_name = models.CharField(max_length=40)
    email = models.EmailField(max_length=40,unique=True)
    enrolled_year = models.DateField(default=timezone.now().date())
    enrolled_session = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    date_created = models.DateField(default=timezone.now().date())
    current_year = models.IntegerField(default=1)

class GradeManagement(models.Model):
    university_id=models.ForeignKey(StudentManagement,on_delete=models.CASCADE)
    course_code= models.ForeignKey(CourseManagement,on_delete=models.CASCADE)
    marks = models.FloatField(default=0)
    grades = models.CharField(max_length=299)
    status = models.CharField(max_length=288)

    def set_grades_and_status(sender,instance,**kwargs):
        if instance.marks >= 80 and instance.marks <= 100:
            instance.status = 'Pass'
            instance.grades = "A"

        elif instance.marks >= 75 and instance.marks <= 79:
            instance.status = 'Pass'
            instance.grades = "A-"

        elif instance.marks >= 70 and instance.marks <= 74:
            instance.status = 'Pass'
            instance.grades = "B+"

        elif instance.marks >= 65 and instance.marks <= 69:
            instance.status = 'Pass'
            instance.grades = "B"

        elif instance.marks >= 60 and instance.marks <= 64:
            instance.status = 'Pass'
            instance.grades= "B-"

        elif instance.marks >= 55 and instance.marks <= 59:
            instance.status = 'Pass'
            instance.grades = "C+"

        elif instance.marks >= 50 and instance.marks <= 54:
            instance.status = 'Pass'
            instance.grades = "C"

        elif instance.marks >= 40 and instance.marks <= 49:
            instance.status = 'Fail'
            instance.grades = "C-"

        elif instance.marks >= 35 and instance.marks <= 39:
            instance.status = 'Fail'
            instance.grades = "D+"

        elif instance.marks >= 33 and instance.marks <= 34:
            instance.status = 'Fail'
            instance.grades = "D"

        elif instance.marks >= 31 and instance.marks <= 32:
            instance.status = 'Fail'
            instance.grades = "D-"

        elif instance.marks >= 0 and instance.marks <= 30:
            instance.status = 'Fail'
            instance.grades = "F"

        else:
            instance.grades = 'NA'
            instance.status = 'NA'
pre_save.connect(GradeManagement.set_grades_and_status,sender=GradeManagement)

class StatusTable(models.Model):
    university_id = models.ForeignKey(StudentManagement,related_name="stud_id",on_delete=models.CASCADE)
    course_code = models.ForeignKey(CourseManagement,on_delete=models.CASCADE)
    session = models.CharField(max_length=299)
    status = models.CharField(max_length=299)

class CourseEnrollment(models.Model):
    univ_id = models.ForeignKey(StudentManagement,on_delete=models.CASCADE)
    courseCode = models.ForeignKey(CourseManagement,on_delete=models.CASCADE)
