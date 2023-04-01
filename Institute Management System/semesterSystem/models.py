import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()
# Create your models here.


class SemesterSystem(models.Model):

    """This model stores necessary data of semester for a  student
        to determine  how much to pay , count of semesters to pay
        , and status info .
        This model is also being used as parent model for SemesterSystemInfo
        to track Semester data"""

    student = models.OneToOneField(User, on_delete=models.CASCADE)
    amount_to_pay = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=50, default='Unpaid')
    session = models.CharField(max_length=50, default='2019-2020')
    department = models.CharField(max_length=300, default='Computer Science and Technology(85)')
    semesters = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.student} semester data'


class SemesterSystemInfo(models.Model):

    """Stores semester wise  data , for all students."""

    semester_student = models.ForeignKey(SemesterSystem, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount_to_pay = models.IntegerField(default=0)
    session = models.CharField(max_length=50, default='')
    department = models.CharField(max_length=200, default='')
    semester = models.IntegerField()
    paid = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='Unpaid')

    def __str__(self):
        return f'Semester data of {self.semester_student} of {self.semester} semester  '


class RegistrationFee(models.Model):

    """Model for storing the data of registration fee
     for a student."""

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_to_pay = models.IntegerField()
    session = models.CharField(max_length=50)
    department = models.CharField(max_length=200)
    paid = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='Unpaid')
    semester = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Registration fee data of {self.student} semester {self.semester}'


class MidTermFee(models.Model):

    """This one stores mid term fee data fro a student."""

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_to_pay = models.IntegerField(default=500)
    session = models.CharField(max_length=50)
    department = models.CharField(max_length=200)
    paid = models.IntegerField(default=0)
    semester = models.IntegerField()
    status = models.CharField(max_length=50, default='Unpaid')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mid terms fee data of {self.student} semester {self.semester}'

