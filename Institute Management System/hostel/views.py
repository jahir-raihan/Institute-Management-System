import datetime

import shortuuid
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from dashboard.models import Transaction
from post.models import Notifications
from .models import User, Hostel, HostelPaymentSystem
from django.http import HttpResponse
from django.db.models import Q
from .algorithms import get_unpaid_hostel_students, distribute_amount, create_transaction


@login_required
def hostel_home(request):

    """Home page of hostel system. Where you can query a hostel
        Student , view the student data and more."""
    notifications = Notifications.objects.order_by('-notification_date')[:10]
    if request.user.is_accountant or request.user.is_admin or request.user.is_hostel_manager:
        if request.method == 'POST':
            key = request.POST['keyword']
            get_student = User.objects.filter(
                Q(registration__startswith=key) | Q(roll__startswith=key) | Q(name__startswith=key)
            ).first()

            if get_student:

                students = Hostel.objects.filter(
                    student=get_student
                )

                return render(request, 'hostel/search_hostel_template.html', {'students': students,
                                                                              'clg_name': settings.COLLEGE_NAME,})
            return HttpResponse('No such student')
        students = get_unpaid_hostel_students(Hostel)

        context = {
            'students': students,
            'notifications': notifications,
            'time': timezone.now(),
            'clg_name': settings.COLLEGE_NAME,
        }
        return render(request, 'hostel/hostel.html', context)
    if request.user.in_hostel:
        student = User.objects.get(pk=request.user.id)
        h_student = Hostel.objects.get(student=student)
        print("student came here")
        return redirect(f'update-hotel-fee/{h_student.id}/')
    return render(request, 'post/404_page_all.html', {'message': "You're not in Hostel.",
                                                      'title': 'Permission denied '})


@login_required
def search_student_to_add(request):

    """This view search students by registrations , roll or name
        to add in hostel ."""

    if request.method == 'POST':
        key = request.POST['keyword']
        if key:

            students = User.objects.filter(
                Q(registration__startswith=key) | Q(roll__startswith=key) | Q(name__startswith=key)
            )

            return render(request, 'hostel/search_student_to_add_template.html', {'students': students,
                                                                                  'clg_name': settings.COLLEGE_NAME,})

    students = User.objects.filter(in_hostel=False)
    context = {
        'students': students,
        'clg_name': settings.COLLEGE_NAME,
    }
    return render(request, 'hostel/search_student_to_add.html', context)


@login_required
def view_student_details(request, pk):

    """Final phase of adding a student to hostel.
        And creating first month hostel data."""
    if request.user.is_admin or request.user.is_accountant or request.user.is_hostel_manager or request.user.is_staff:
        if request.method == 'POST':
            student = User.objects.get(pk=request.POST['student_id'])
            student.in_hostel = True
            h = Hostel(student=student)
            hs = HostelPaymentSystem(hostel_student=h, date=datetime.datetime.now(), amount_to_pay=settings.HOSTEL_FEE,
                                     session=student.session, semester=student.semester, department=student.department)

            h.save()
            student.save()
            hs.save()

            context = {
                'student': student,
                'user_created': student,
                'message': True,
                'clg_name': settings.COLLEGE_NAME,

            }
            return render(request, 'hostel/view_details.html', context)

        student = User.objects.get(pk=pk)
        context = {
            'student': student,
            'clg_name': settings.COLLEGE_NAME,
        }
        return render(request, 'hostel/view_details.html', context)
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission to enter this page.",
                                                      'title': 'Permission denied '})


@login_required
def update_hostel_fee(request, pk):

    """This view gets called when a student pays for hostel fee.
        It calls distribute_amount function from algorithms.py
        to distribute the paid amount among all hostel data month."""
    notifications = Notifications.objects.order_by('-notification_date')[:10]
    if request.user.is_accountant:
        if request.method == 'POST' and request.user.is_accountant:

            student = Hostel.objects.get(pk=request.POST['student'])
            distribute_amount(student.hostelpaymentsystem_set.filter(status='Unpaid'), int(request.POST['amount']))

            r_id = shortuuid.ShortUUID().random(25)

            trans = Transaction(recipient_student=student.student, receipt_id=r_id, recipient=student.student.name,
                                signature_of_student=student.student.name,
                                signature_of_accountant=request.user.name,
                                email=student.student.email, transaction_type='Cash In')
            trans.student_roll = student.student.roll
            trans.department = student.student.department
            trans.semester = student.student.semester
            trans.save()
            trans.custom_receipt_id = trans.id + 1000
            create_transaction(trans, 'Hostel Fee', int(request.POST['amount']), request)

            var = get_unpaid_hostel_students(Hostel)

            get_student = Hostel.objects.get(pk=pk)

            disable_inputs = False
            if get_student.amount_to_pay == 0:
                disable_inputs = True

            context = {
                'disable_inputs': disable_inputs,
                'student': get_student,
                'clg_name': settings.COLLEGE_NAME,
            }
            return render(request, 'hostel/updated_payment_template.html', context)
        get_unpaid_hostel_students(Hostel)
        student = Hostel.objects.get(pk=pk)
        disable_inputs = False
        if student.amount_to_pay == 0:
            disable_inputs = True
        context = {
            'disable_inputs': disable_inputs,
            'student': student,
            'notifications': notifications,
            'time': timezone.now(),
            'clg_name': settings.COLLEGE_NAME,
        }
        return render(request, 'hostel/update_hostel_fee.html', context)
    if request.user.in_hostel:
        student = Hostel.objects.get(pk=pk)
        context = {

            'student': student,
            'notifications': notifications,
            'time': timezone.now(),
            'clg_name': settings.COLLEGE_NAME,
        }

        return render(request, 'hostel/update_hostel_fee.html', context)
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission to enter this page.",
                                                      'title': 'Permission denied '})
