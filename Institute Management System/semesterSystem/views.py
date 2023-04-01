import shortuuid
from django.shortcuts import render
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.conf import settings
from dashboard.models import Transaction
from hostel.algorithms import create_transaction
from post.models import Notifications
from user.forms import UserRegisterForm
from .models import User, SemesterSystem, SemesterSystemInfo
from django.http import HttpResponse
from django.db.models import Q
from .algorithms import get_unpaid_semester_students, distribute_amount


@login_required
def semester_home(request):

    """Home page of semester system. Where you can query a
        Student , view the student data and do more things."""
    notifications = Notifications.objects.order_by('-notification_date')[:10]
    if request.user.is_accountant:
        if request.method == 'POST':
            key = request.POST['keyword']
            get_student = User.objects.filter(
                Q(registration__startswith=key) | Q(roll__startswith=key) | Q(name__startswith=key)
            ).first()

            if get_student:

                students = SemesterSystem.objects.filter(
                    student=get_student
                )

                return render(request, 'semesterSystem/search_semester_template.html', {'students': students,
                                                                                        'clg_name': settings.COLLEGE_NAME,})
            return HttpResponse('No such student')
        students = get_unpaid_semester_students(SemesterSystem)

        context = {
            'students': students,
            'notifications': notifications,
            'time': timezone.now(),
            'clg_name': settings.COLLEGE_NAME,
        }
        return render(request, 'semesterSystem/semester.html', context)
    if request.user.is_student:
        get_student = User.objects.get(pk=request.user.id)
        student = SemesterSystem.objects.get(student=get_student)
        return redirect(f'update-semester-fee/{student.id}/')
    else:
        return render(request, 'post/404_page_all.html', {'message': "You're not a student.",
                                                          'title': 'Not a student'})


@login_required
def update_semester_fee(request, pk):

    """This view gets called when a student pays for semester fee.
        It calls distribute_amount function from algorithms.py
        to distribute the paid amount among all semesters that needs to be paid."""
    notifications = Notifications.objects.order_by('-notification_date')[:10]
    if request.user.is_accountant:
        if request.method == 'POST' and request.user.is_accountant:

            student = SemesterSystem.objects.get(pk=request.POST['student'])
            distribute_amount(student.semestersysteminfo_set.order_by('semester').filter(status='Unpaid'), int(request.POST['amount']))

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
            create_transaction(trans, 'Semester Fee', int(request.POST['amount']), request)

            var = get_unpaid_semester_students(SemesterSystem)

            get_student = SemesterSystem.objects.get(pk=pk)

            disable_inputs = False
            if get_student.amount_to_pay == 0:
                disable_inputs = True

            context = {
                'disable_inputs': disable_inputs,
                'student': get_student,
                'notifications': notifications,
                'clg_name': settings.COLLEGE_NAME,
            }
            return render(request, 'semesterSystem/updated_payment_template.html', context)
        get_unpaid_semester_students(SemesterSystem)
        student = SemesterSystem.objects.get(pk=pk)
        disable_inputs = False
        if student.amount_to_pay == 0:
            disable_inputs = True
        context = {
            'disable_inputs': disable_inputs,
            'student': student,
            'clg_name': settings.COLLEGE_NAME,
        }
        return render(request, 'semesterSystem/update_semester_fee.html', context)
    if request.user.is_student:
        get_unpaid_semester_students(SemesterSystem)
        student = SemesterSystem.objects.get(pk=pk)

        context = {

            'student': student,
            'clg_name': settings.COLLEGE_NAME,
        }
        return render(request, 'semesterSystem/update_semester_fee.html', context)
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission to enter this page.",
                                                      'title': 'Permission denied'})
# views for adding previous semester data of a student


def add_prev_semester_data(request):

    """This view is for adding previous semester data's of student.
        for example if a student registers in the site while his in 3rd
        semester then where do we will get previous 2 semester data?
        That's why this view is."""

    if request.user.is_accountant or request.user.is_admin:
        if request.method == 'POST':
            student = User.objects.filter(roll=request.POST['roll']).first()
            if student:
                semester_obj = SemesterSystem.objects.get(student=student)
                try:
                    data = SemesterSystemInfo.objects.get(semester_student=semester_obj,
                                                          semester=request.POST['semester'])
                    return render(request, 'semesterSystem/add_prev_s_data_success_template.html',
                                  {'error': True, 'msg': 'Semester Data Already Exist.'})
                except:
                    amount_to_pay = int(request.POST['amount_to_pay'])
                    paid = int(request.POST['paid'])
                    data = SemesterSystemInfo(semester_student=semester_obj,
                                              amount_to_pay=amount_to_pay,
                                              paid=paid, semester=int(request.POST['semester']),
                                              session=student.session, department=student.department
                                              )
                    data.save()
                    if amount_to_pay - paid == 0:
                        data.status = 'Paid'
                        data.save()
                    return render(request, 'semesterSystem/add_prev_s_data_success_template.html',
                                  {'error': False, 'msg': f'Added Semester Data for {student.roll} Successfully'})
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission ",
                                                      'title': 'Permission denied'})


def refresh_add_prev_s_data_form(request):

    """Helper view for refreshing Add Previous Semester data form ,
        without losing state."""

    form = UserRegisterForm()
    context = {
        'form': form,
        'time': timezone.now(),
        'clg_name': settings.COLLEGE_NAME,
    }
    return render(request, 'semesterSystem/refresh_add_prev_s_template.html', context)