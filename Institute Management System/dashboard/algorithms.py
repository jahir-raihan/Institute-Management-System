from datetime import datetime
from email.mime.image import MIMEImage
from django.shortcuts import render
from .models import TransactionDetails, StatementHistory, ParentContainerArrears, DataContainerArrears, \
    SubContainerArrears
from hostel.algorithms import distribute_amount as h_d_amount
from semesterSystem.algorithms import distribute_amount as s_d_amount
from hostel.models import Hostel, HostelPaymentSystem
from semesterSystem.models import SemesterSystem, RegistrationFee, MidTermFee, SemesterSystemInfo
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import os

#   imports for statement section


def save_trans_reasons(trans, reason, amount, request):

    """This one saves the transaction  reasons with their amount .
        Also if semester , hostel , registration or mid term fee
        encounters this algo will also update the information of
        those things."""

    trans.total_amount = sum(list(map(int, amount)))
    trans.save()
    trans_reason = ""
    for i in range(len(reason)):
        if TransactionDetails.objects.filter(transaction=trans, transaction_reason=reason[i]).first() is not None:
            temp = TransactionDetails.objects.filter(transaction=trans, transaction_reason=reason[i]).first()
            temp.transaction_amount += int(amount[i])
            temp.save()
        else:

            if reason[i] == 'Others' and 'other_reason' in request.POST:
                trans_det = TransactionDetails(transaction=trans,
                                               transaction_reason=f'{reason[i]} ({request.POST["other_reason"]})',
                                               transaction_amount=amount[i])
                trans_det.save()
                continue
            else:
                trans_det = TransactionDetails(transaction=trans, transaction_reason=reason[i],
                                               transaction_amount=amount[i])
                trans_det.save()
            trans_reason += reason[i] + ', '
        if reason[i] == 'Semester Fee':
            student = trans.recipient_student
            semester_obj = SemesterSystem.objects.get(student=student)

            s_d_amount(semester_obj.semestersysteminfo_set.order_by('semester').filter(status='Unpaid'), int(amount[i]))

        elif reason[i] == 'Hostel Fee':
            student = trans.recipient_student
            hostel_obj = Hostel.objects.get(student=student)
            h_d_amount(hostel_obj.hostelpaymentsystem_set.order_by('-date').filter(status='Unpaid'), int(amount[i]))

        elif reason[i] == 'Form Fill Up Fee':
            student = trans.recipient_student
            reg_obj = RegistrationFee.objects.order_by('-date').filter(student=student, semester=student.semester,
                                                                       status='Unpaid').first()
            reg_obj.paid = int(amount[i])
            reg_obj.status = 'Paid'
            reg_obj.save()
        elif reason[i] == 'Mid Semester Fee':
            student = trans.recipient_student
            reg_obj = MidTermFee.objects.order_by('-date').filter(student=student, semester=student.semester,
                                                                  status='Unpaid').first()
            reg_obj.paid = int(amount[i])
            reg_obj.status = 'Paid'
            reg_obj.save()

    context = {
        "trans_reason": trans_reason,
        "receipt_id": trans.receipt_id,
        "custom_receipt_id": trans.custom_receipt_id,
        'year': datetime.now().year,
        'clg_name': settings.COLLEGE_NAME,
        'domain': request.META['HTTP_HOST']
    }
    html_content = render_to_string('emailTemplate/receipt_email.html', context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        f"Transaction Receipt  of {trans_reason} due {trans.date}. ",
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


def determine_cash_in_cash_out(data):

    """This algorithm determines total cash in and cash out
        amount from transaction data."""

    total_cash_in = 0
    total_cash_out = 0
    for d in data:
        if d.transaction_type == 'Cash In':
            total_cash_in += d.total_amount
        elif d.transaction_type == 'Cash Out':
            total_cash_out += d.total_amount
    return [total_cash_in, total_cash_out]


def get_number_in_text(n):

    """This algorithm converts integer numbers to word numbers."""

    number = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    nty = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    tens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]

    if n > 99999:
        return 'Not possible'
    else:
        d = [0, 0, 0, 0, 0]
        i = 0
        while n > 0:
            d[i] = n % 10
            i += 1
            n = n//10
        num = ""
        if d[4] != 0:
            if d[4] == 1:
                num += tens[d[3]] + " Thousand "
            else:
                num += nty[d[4]]+" "+number[d[3]] + " Thousand "
        else:
            if d[3] != 0:
                num += number[d[3]] + " Thousand "
        if d[2] != 0:
            num += number[d[2]]+" Hundred "
        if d[1] != 0:
            if d[1] == 1:
                num += tens[d[0]]
            else:
                num += nty[d[1]] + " " + number[d[0]]
        else:
            if d[0] != 0:
                num += number[d[0]]
        return num


#  algorithms for statement section in transaction

def get_statement_data(request, request1, f_type):

    """This algorithm saves StatementHistory data for generating
        Fee statement data in future."""

    data = None
    if f_type == 'Mid Term Fee':

        data = MidTermFee.objects.filter(session=request1['session'], department=request1['department'],
                                         semester=request1['semester'])

    elif f_type == 'Form Fill Up Fee':
        data = RegistrationFee.objects.filter(session=request1['session'], department=request1['department'],
                                              semester=request1['semester'])
    elif f_type == 'Semester Fee':
        data = SemesterSystemInfo.objects.filter(session=request1['session'], department=request1['department'],
                                                 semester=request1['semester'])

    if data:
        statement = StatementHistory(session=request1['session'], department=request1['department'],
                                     semester=request1['semester'], f_type=f_type, generated_by=request.user,
                                     title=f_type)
        statement.save()
        context = {
            'found': True,
            'path_name': 'get_statement_link',
            'id': statement.id
        }
        return render(request, 'dashboard/transaction/statement_template.html', context)
    return render(request, 'dashboard/transaction/statement_template.html', {'found': False})


def return_semester(s):

    """Returns numbered semester in string semester"""

    dic = {
        1: '1st',
        2: '2nd',
        3: '3rd',
        4: '4th',
        5: '5th',
        6: '6th',
        7: '7th'
    }
    return dic[s]

#   For arrears sheet


def get_all_fee_data(request, request1, f_type):

    """This view saves a statement for generating arrears data."""

    data = SemesterSystem.objects.filter(session=request1['session'], department=request1['department'])
    if data:
        statement = StatementHistory(session=request1['session'], department=request1['department'],
                                     semester=request1['semester'], f_type=f_type, generated_by=request.user,
                                     title=f_type)
        statement.save()
        context = {
            'found': True,
            'path_name': 'get_statement_link',
            'id': statement.id
        }
        return render(request, 'dashboard/transaction/statement_template.html', context)
    return render(request, 'dashboard/transaction/statement_template.html', {'found': False})


#   algo for getting student data


def get_student_data(statement):

    """This algorithm gets all arrears fee data of students , saves the
        data in a container model and returns the container to use in
        template."""

    semester_data = SemesterSystem.objects.filter(session=statement.session,
                                                  department=statement.department)
    ParentContainerArrears.objects.all().delete()
    container = ParentContainerArrears(session=statement.session, semester=statement.semester,
                                       department=statement.department)
    container.save()
    for data in semester_data:
        data_container_arrears = DataContainerArrears(parent=container, name=data.student.name, roll=data.student.roll,
                                                      registration=data.student.registration, total=0, current=0)
        data_container_arrears.save()

        data1 = data.semestersysteminfo_set.order_by('semester')
        for d in data1:
            mid_amount = 0
            reg_amount = 0
            semester_amount = d.amount_to_pay - d.paid

            mid = MidTermFee.objects.filter(session=statement.session, department=statement.department,
                                            semester=d.semester, student=d.semester_student.student).first()

            if mid:
                mid_amount = mid.amount_to_pay - mid.paid

            reg = RegistrationFee.objects.filter(session=statement.session, department=statement.department,
                                                 semester=d.semester, student=d.semester_student.student).first()

            if reg:

                reg_amount = reg.amount_to_pay - reg.paid

            total = mid_amount + reg_amount + semester_amount
            data_container_arrears.total += total
            data_container_arrears.current += total
            data_container_arrears.save()
            sub_container_arrears = SubContainerArrears(data_container=data_container_arrears,
                                                        semester=d.semester)
            if total == 0:

                sub_container_arrears.total_amount = 'F.P'

            else:

                sub_container_arrears.total_amount = str(total)

            sub_container_arrears.save()
    return container


def get_semester_in_word(s):

    """Getting semester in word by a range"""

    res = []
    for i in range(1, s+1):
        res.append(return_semester(i))
    return res


def calculate_total_mid_reg(object):

    """Small helper function to calculate total amount of
        Mid Term and Form Fill Up Fee."""

    total = 0
    for obj in object:
        total += obj.amount_to_pay - obj.paid
    return total
