from django.db import models
import datetime
from django.contrib.auth import get_user_model

User = get_user_model()


class Hostel(models.Model):

    """This model stores necessary data of a hostel student
        to determine  how much to pay , count of months to pay
        , and status info .
        This model is also being used as parent model for HostelPaymentInfo
        to track monthly data"""

    student = models.OneToOneField(User, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=30, default='Unpaid')
    months = models.IntegerField(default=0)
    amount_to_pay = models.IntegerField(default=0)
    last_payment = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.student} hostel data'


class HostelPaymentSystem(models.Model):

    """Stores monthly hostel data , for hostel students."""

    hostel_student = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    date = models.DateField()
    amount_to_pay = models.IntegerField(default=0)
    session = models.CharField(max_length=50, default='')
    department = models.CharField(max_length=200, default='')
    semester = models.IntegerField()
    paid = models.IntegerField(default=0)
    status = models.CharField(max_length=30, default='Unpaid')

    def __str__(self):
        return f'{self.hostel_student} ({self.date})  hostel data'
# Create your models here.
