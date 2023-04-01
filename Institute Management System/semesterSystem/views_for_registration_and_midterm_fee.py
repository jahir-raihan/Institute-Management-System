import shortuuid
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings
from dashboard.models import Transaction
from hostel.algorithms import create_transaction
from post.models import Notifications
from .models import RegistrationFee, MidTermFee
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q

User = get_user_model()


@login_required
def registration_home(request):
    notifications = Notifications.objects.order_by('-notification_date')[:10]
    if request.user.is_accountant:
        if request.method == 'POST':
            key = request.POST['keyword']
            if key:
                get_student = User.objects.filter(
                    Q(registration__startswith=key) | Q(roll__startswith=key) | Q(name__startswith=key) | Q(semester=key)
                ).first()

                if get_student:
                    students = RegistrationFee.objects.filter(
                        student=get_student, semester=get_student.semester
                    )

                    return render(request, 'semesterSystem/registration/search_registration_student.html',
                                  {'students': students, 'clg_name': settings.COLLEGE_NAME,})
            else:
                students = RegistrationFee.objects.order_by('-semester')
                context = {
                    'students': students,
                    'clg_name': settings.COLLEGE_NAME,
                }
                return render(request, 'semesterSystem/registration/search_registration_student.html', context)

        students = RegistrationFee.objects.filter(status='Unpaid')

        context = {
            'students': students,
            'notifications': notifications,
            'time': timezone.now(),
            'clg_name': settings.COLLEGE_NAME,
        }
        return render(request, 'semesterSystem/registration/registration_home.html', context)
    if request.user.is_student:
        get_student = User.objects.get(pk=request.user.id)
        student = RegistrationFee.objects.filter(student=get_student).first()
        if student:
            return redirect(f'/semester-system/registration/update-registration-fee/{student.id}/')
        else:
            return render(request, 'post/404_page_all.html', {'message': 'No Registration Data Yet.', 'title': 'No data'})
    else:
        return render(request, 'post/404_page_all.html', {'message': "You're not a student.",
                                                          'title': 'Not a student'})


@login_required
def update_registration_fee(request, pk):
    notifications = Notifications.objects.order_by('-notification_date')[:10]
    if request.user.is_accountant:
        if request.method == 'POST':
            student = RegistrationFee.objects.get(pk=pk)
            student.paid = int(request.POST['amount'])
            student.status = 'Paid'
            student.save()

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
            create_transaction(trans, 'Form Fill Up Fee', int(request.POST['amount']), request)

            context = {
                'student': student,
                'disable_inputs': True,
                'clg_name': settings.COLLEGE_NAME,
            }

            return render(request, 'semesterSystem/registration/view_registration_fee_data_template.html', context)

        student = RegistrationFee.objects.get(pk=pk)
        disable_inputs = False
        if student.amount_to_pay == student.paid:
            disable_inputs = True

        context = {
            'student': student,
            'disable_inputs': disable_inputs,
            'notifications': notifications,
            'time': timezone.now(),
            'clg_name': settings.COLLEGE_NAME,
        }
        return render(request, 'semesterSystem/registration/view_registration_fee_data.html', context)
    if request.user.is_student:
        student = RegistrationFee.objects.get(pk=pk)
        context = {
            'student': student,
            'notifications': notifications,
            'time': timezone.now(),
            'clg_name': settings.COLLEGE_NAME,
        }
        return render(request, 'semesterSystem/registration/view_registration_fee_data.html', context)
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission to enter this page.",
                                                      'title': 'Permission denied'})

# views for mid term fees.


@login_required
def midterm_home(request):

    """Mid term fee system home . You can manage student's info
        at here or add update query , anything you want."""

    notifications = Notifications.objects.order_by('-notification_date')[:10]
    if request.user.is_accountant:
        if request.method == 'POST':
            key = request.POST['keyword']
            if key:
                get_student = User.objects.filter(
                    Q(registration__startswith=key) | Q(roll__startswith=key) | Q(name__startswith=key) | Q(semester=key)
                ).first()

                if get_student:
                    students = MidTermFee.objects.filter(
                        student=get_student, semester=get_student.semester
                    )

                    return render(request, 'semesterSystem/midterm/search_midterm_student.html',
                                  {'students': students, 'clg_name': settings.COLLEGE_NAME,})
            else:
                students = MidTermFee.objects.order_by('-semester')
                context = {
                    'students': students,
                    'clg_name': settings.COLLEGE_NAME,
                }
                return render(request, 'semesterSystem/midterm/search_midterm_student.html', context)

        students = MidTermFee.objects.filter(status='Unpaid')

        context = {
            'notifications': notifications,
            'time': timezone.now(),
            'students': students,
            'clg_name': settings.COLLEGE_NAME,
        }
        return render(request, 'semesterSystem/midterm/midterm_home.html', context)
    if request.user.is_student:
        get_student = User.objects.get(pk=request.user.id)
        student = MidTermFee.objects.filter(student=get_student).first()
        if student:
            return redirect(f'/semester-system/midterm/update-midterm-fee/{student.id}/')
        else:
            return render(request, 'post/404_page_all.html', {'message': 'No Mid Term Data Yet.', 'title': 'No data'})
    else:
        return render(request, 'post/404_page_all.html', {'message': "You're not a student.",
                                                          'title': 'Not a student'})


@login_required
def update_midterm_fee(request, pk):

    """This view updates mid term fee information.
        Only active students data will get update."""

    notifications = Notifications.objects.order_by('-notification_date')[:10]
    if request.user.is_accountant:
        if request.method == 'POST':
            student = MidTermFee.objects.get(pk=pk)
            student.paid = int(request.POST['amount'])
            student.status = 'Paid'
            student.save()

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
            create_transaction(trans, 'Mid Semester Fee', int(request.POST['amount']), request)

            context = {
                'student': student,
                'disable_inputs': True,
                'clg_name': settings.COLLEGE_NAME,
            }

            return render(request, 'semesterSystem/midterm/view_midterm_fee_data_template.html', context)

        student = MidTermFee.objects.get(pk=pk)
        disable_inputs = False
        if student.amount_to_pay == student.paid:
            disable_inputs = True

        context = {
            'notifications': notifications,
            'time': timezone.now(),
            'student': student,
            'disable_inputs': disable_inputs,
            'clg_name': settings.COLLEGE_NAME,
        }
        return render(request, 'semesterSystem/midterm/view_midterm_fee_data.html', context)
    if request.user.is_student:
        student = MidTermFee.objects.get(pk=pk)
        context = {
            'notifications': notifications,
            'time': timezone.now(),
            'student': student,

            'clg_name': settings.COLLEGE_NAME,
        }
        return render(request, 'semesterSystem/midterm/view_midterm_fee_data.html', context)
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission to enter this page.",
                                                      'title': 'Permission denied.'})


#   Rest code will be for updating  Midterm and Registration fee data

def authenticate_user_to_update_midterm_info(request):
    """This will authenticate the user while updating mid term fee .
           Only admin can access this view by verification ."""

    if request.method == 'POST' and request.user.is_admin:
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
        if user and user.is_admin:
            return render(request, 'semesterSystem/midterm/update_mid_term_fee_template.html', {'clg_name': settings.COLLEGE_NAME, })


def update_midterm_info(request):
    """This view updates Mid term Fee data for every single active student in the college."""

    if request.method == 'POST' and request.user.is_admin:
        students = User.objects.filter(is_student=True, is_deafen=False)
        for student in students:
            mid = MidTermFee(student=student, semester=student.semester, amount_to_pay=int(request.POST['amount']),
                             session=student.session, department=student.department)
            mid.save()

        return HttpResponse('<p style="color:black;text-align:center; '
                            'height:200px; margin-top:35%;">Updated Mid Term Data Successfully</p>')
    return False


def authenticate_user_to_update_registration_info(request):
    """This will authenticate the user while updating registration fee .
           Only admin can access this view by verification ."""

    if request.method == 'POST' and request.user.is_admin:
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
        if user and user.is_admin:
            return render(request, 'semesterSystem/registration/update_reg_fee_template.html', {'clg_name': settings.COLLEGE_NAME, })


def update_registration_info(request):

    """This view updates Registration data of every single active student in college."""
    if request.method == 'POST' and request.user.is_admin:
        students = User.objects.filter(is_student=True, is_deafen=False)
        for student in students:
            registrations = RegistrationFee(student=student, amount_to_pay=int(request.POST['amount']),
                                            session=student.session, department=student.department,
                                            semester=student.semester)
            registrations.save()

        return HttpResponse('<p style="color:black;text-align:center; '
                            'height:200px; margin-top:35%;">Updated Form Fill Up Data Successfully</p>')
    return False