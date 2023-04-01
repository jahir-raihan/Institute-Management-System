from django.utils import timezone

from .models import SemesterSystem
import datetime


def get_unpaid_semester_students(semester_system):

    """This algorithm determines how much to pay , is it paid or not
        , sets the payment status based on some calculations on each semester ."""

    for data in semester_system.objects.all():
        get_stat = data.semestersysteminfo_set.filter(status='Unpaid')

        if len(get_stat) > 0:
            data.payment_status = 'Unpaid'
            data.semesters = len(get_stat)
            data.amount_to_pay = set_amount_to_pay(get_stat)

            data.save()

        else:
            data.payment_status = 'Paid'
            data.semesters = len(get_stat)
            data.amount_to_pay = 0

            data.save()
    return semester_system.objects.filter(payment_status='Unpaid')


def set_amount_to_pay(semester_data):

    """This function is a helper function to determine
        total amount to pay."""

    total = 0
    for data in semester_data:
        total += data.amount_to_pay - data.paid
    return total


def distribute_amount(semester_data, amount):

    """When a student pays for semester fee , this function
        distributes the amount among all semester and
        sets the payment status by calculation."""

    amount = amount

    for data in semester_data:

        temp = data.amount_to_pay - data.paid
        if amount > temp:
            data.paid += temp
            amount -= temp

        elif amount == temp or amount < temp:
            data.paid += amount
            amount = 0

        data.save()
        set_status(data)


def set_status(data):

    """Helper function to set the status of semester payment info."""

    if data.amount_to_pay == data.paid:
        data.status = 'Paid'
        data.save()

