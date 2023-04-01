import os
from datetime import datetime
from email.mime.image import MIMEImage

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from dashboard.models import TransactionDetails


def get_unpaid_hostel_students(hostel):

    """This algorithm determines how much to pay , is it paid or not
        , sets the payment status based on some calculations on each month ."""

    for data in hostel.objects.all():
        get_stat = data.hostelpaymentsystem_set.filter(status='Unpaid')

        if len(get_stat) > 0:
            data.payment_status = 'Unpaid'
            data.months = len(get_stat)
            data.amount_to_pay = set_amount_to_pay(get_stat)
            data.save()

        else:
            data.payment_status = 'Paid'
            data.months = len(get_stat)
            data.amount_to_pay = 0

            data.save()
    return hostel.objects.filter(payment_status='Unpaid')


def set_amount_to_pay(month_data):

    """This function is a helper function to determine
        total amount to pay."""

    total = 0
    for data in month_data:
        total += data.amount_to_pay - data.paid
    return total


def distribute_amount(hostel_data, amount):

    """When a student pays for hostel fee , this function
        distributes the amount among all hostel months and
        sets the payment status by calculation."""

    amount = amount

    for data in hostel_data:
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

    """Helper function to set the status."""

    if data.amount_to_pay == data.paid:
        data.status = 'Paid'
        data.save()


def create_transaction(trans, reason, amount, request):
    trans.total_amount = amount
    trans.save()
    trans_det = TransactionDetails(transaction=trans, transaction_reason=reason, transaction_amount=amount)
    trans_det.save()

    context = {
        "trans_reason": reason,
        "receipt_id": trans.receipt_id,
        "custom_receipt_id": trans.custom_receipt_id,
        'year': datetime.now().year,
        'clg_name': settings.COLLEGE_NAME,
        'domain': request.META['HTTP_HOST'],
    }
    html_content = render_to_string('emailTemplate/receipt_email.html', context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        f"Transaction Receipt  of {reason} due {trans.date}. ",
        text_content,
        settings.EMAIL_HOST_USER,
        [trans.email, ]
    )
    path = settings.EMAIL_LOGO_PATH  # path to your logo
    image = 'Logo.jpg'  # logo name
    email.attach_alternative(html_content, 'text/html')
    file_path = os.path.join(path, image)
    with open(file_path, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-ID', '<{name}>'.format(name=image))
        img.add_header('Content-Disposition', 'inline', filename=image)

    email.attach(img)
    email.send()
