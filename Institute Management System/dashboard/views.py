import datetime
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from collegeSystem.algorithms import get_session_year_list, determine_grade, determine_total_gpa_point
from collegeSystem.forms import GetResultFormValidation, UploadResultForm
from semesterSystem.models import MidTermFee, RegistrationFee
from post.models import Notifications
from django.utils import timezone
from semesterSystem.algorithms import get_unpaid_semester_students
from hostel.algorithms import get_unpaid_hostel_students
from django.db.models import Q
from user.forms import UserRegisterForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

# imports from semester System
from semesterSystem.models import SemesterSystem , SemesterSystemInfo

# imports from hostel system
from hostel.models import Hostel, HostelPaymentSystem

# import from college system
from collegeSystem.models import UploadResult, Result, StoreGrade

User = get_user_model()


@login_required
def dashboard_home(request):

    """This view is dashboard home , by default
        this view will render semester system.
        Rest of other system pages will load in
        the background using ajax."""
    notifications = Notifications.objects.order_by('-notification_date')[:10]
    if request.user.is_admin:
        if request.method == 'POST':
            key = request.POST['keyword']
            if key != '':
                get_student = User.objects.filter(
                    Q(registration__startswith=key) | Q(roll__startswith=key) | Q(name__startswith=key)
                ).first()

                if get_student:
                    students = SemesterSystem.objects.filter(
                        student=get_student
                    )

                    return render(request, 'dashboard/dashboard_semester_template.html', {'students': students})
                return HttpResponse('No data found')

            students = SemesterSystem.objects.filter(payment_status='Unpaid')

            return render(request, 'dashboard/dashboard_semester_template.html', {'students': students})
        students = get_unpaid_semester_students(SemesterSystem)
        session_year_list = sorted(get_session_year_list(datetime.datetime.now().year), reverse=True)
        form = UserRegisterForm()
        context = {
            'students': students,
            'form': form,
            'session_year_list': session_year_list,
            'notifications': notifications,
            'time': timezone.now(),
            'clg_name': settings.COLLEGE_NAME,
        }
        return render(request, 'dashboard/dashboard_semester.html', context)
    else:
        return render(request, 'post/404_page_all.html', {'message': "You don't have permission to enter this page.",
                                                          'title': 'Permission denied '})


@login_required
def college_user_system(request):

    """This one handles both teacher and student in one place.
        Only admin can access this page and can create new teacher or
        student in the site."""
    if request.user.is_admin:

        if request.method == 'POST':

            key = request.POST['keyword']
            if key:

                students = User.objects.filter(
                    Q(registration__startswith=key) | Q(roll__startswith=key) | Q(name__startswith=key)
                )

                return render(request, 'dashboard/college_user_student_template.html', {'students': students,
                                                                                        'clg_name': settings.COLLEGE_NAME,})
            students = User.objects.filter(is_teacher=False)
            return render(request, 'dashboard/college_user_student_template.html', {'students': students,
                                                                                    'clg_name': settings.COLLEGE_NAME,})
        return False
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission.",
                                                      'title': 'Permission denied '})


@login_required
def dashboard_hostel(request):

    """This one belongs to hostel system.
        Where hostel manager can update hostel
        students data , add a student to hostel or
        updating the hostel data by month for monthly
        hostel fee."""

    if request.method == 'POST':
        key = request.POST['keyword']
        get_student = User.objects.filter(
            Q(registration__startswith=key) | Q(roll__startswith=key) | Q(name__startswith=key)
        ).first()

        if get_student:

            students = Hostel.objects.filter(
                student=get_student
            )

            return render(request, 'dashboard/dashboard_hostel_template.html', {'students': students,
                                                                                'clg_name': settings.COLLEGE_NAME,})
        return HttpResponse('No such student')


@login_required
def redirect_template_view(request):

    """This view plays a key role in navigation from one
        page to another without page refreshment using ajax.
        Mainly this view works on link based id's .
        When a particular id is encountered  desired page will
        be sent as HttpResponse to frontend/ajax."""

    if request.method == 'POST' and request.POST['link_id'] != '':
        link_id = request.POST['link_id']
        if link_id == '1':
            students = get_unpaid_semester_students(SemesterSystem)

            # test program block

            context = {
                'students': students,
                'clg_name': settings.COLLEGE_NAME,
            }

            return render(request, 'dashboard/dashboard_semester_link_template.html', context)

        if link_id == '2':

            students = get_unpaid_hostel_students(Hostel)

            # test program block

            context = {
                'students': students,
                'clg_name': settings.COLLEGE_NAME,
            }

            return render(request, 'dashboard/dashboard.html', context)

        if link_id == '3':
            students = User.objects.filter(is_teacher=False)

            teachers = User.objects.filter(is_teacher=True)
            context = {
                'students': students,
                'teachers': teachers,
                'clg_name': settings.COLLEGE_NAME,

            }
            return render(request, 'dashboard/college_user.html', context)

    else:
        return False

# Semester System Management


@login_required
def authenticate_to_update_semester_data(request):

    """This will authenticate the user while updating semester .
        Ex: current semester is 4  and needs to be updated to 5.
        Only admin can access this view by validation ."""

    if request.method == 'POST' and request.user.is_admin:
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
        if user and user.is_admin:
            return render(request, 'dashboard/update_semester_template.html', {'clg_name': settings.COLLEGE_NAME,})
        return HttpResponse('<p style="color:rgb(255, 102, 42);'
                            ' text-align:center; height:200px; margin-top:35%;">Authentication Failed.</p>')


@login_required
def authenticate_to_update_hostel_data(request):

    """This one also works same as above , little
        change is that hostel manager can also
        access this view."""

    if request.method == 'POST' and request.user.is_admin:
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
        if user and user.is_admin or user.is_hostel_manager:
            return render(request, 'dashboard/update_hostel_data_template.html', {'clg_name': settings.COLLEGE_NAME,})


@login_required
def update_semester(request):

    """After authenticating admin user .
        This view will update the semester
        of all existing students."""

    if request.method == 'POST' and request.user.is_admin:
        students = User.objects.filter(is_student=True, is_deafen=False)
        for student in students:

            student.semester += 1
            student.save()

            semester = SemesterSystem.objects.get(student=student)
            semester_info = SemesterSystemInfo(semester_student=semester, amount_to_pay=settings.SEMESTER_FEE,
                                               session=student.session, semester=student.semester,
                                               department=student.department)
            if student.has_disability or student.father_is_dead or student.special_discount:
                semester_info.amount_to_pay = semester_info.amount_to_pay // 2
            semester_info.save()

        return HttpResponse('<p style="color:black;text-align:center; '
                            'height:200px; margin-top:35%;">Updated Semester Successfully</p>')
    return False


@login_required
def update_hostel(request):

    """After authenticating admin/hostel manager
        This view will update the monthly hostel data
        of hostel students."""

    if request.method == 'POST' and request.user.is_admin:
        students = User.objects.filter(in_hostel=True, is_deafen=False)
        for student in students:

            h = Hostel.objects.get(student=student)

            hs = HostelPaymentSystem(hostel_student=h, date=datetime.datetime.now(),
                                     amount_to_pay=settings.HOSTEL_FEE, semester=student.semester,
                                     session=student.session, department=student.department)
            hs.save()

        return HttpResponse('<p style="color:black;text-align:center; '
                            'height:200px; margin-top:35%;">Updated Hostel Data Successfully</p>')
    return False


# view for tabulation

def get_context_data():

    """It seems that we where repeating our codes below for
        filtering mark sheet file , tabulation file and
        short mark sheet file . To avoid this repetition
        this function will be used as helper function for context
        data ."""
    session_year_list = sorted(get_session_year_list(datetime.datetime.now().year), reverse=True)

    form = GetResultFormValidation()
    form2 = UploadResultForm()
    context = {
        'form': form,
        'form2': form2,
        'session_year_list': session_year_list,
        'clg_name': settings.COLLEGE_NAME,
    }
    return context


@login_required
def tabulation_filter(request):

    """This view filters tabulation sheet and returns the id of the file.
        Only admin can access this page."""

    if request.user.is_admin:
        if request.method == 'POST':
            file = UploadResult.objects.filter(session=request.POST['session'], which_semester=request.POST['semester'],

                                               department=request.POST['department']).order_by('-session_year').first()
            found = False
            if file:
                found = True
                return render(request, 'dashboard/tabulation/sheet_template.html',
                              {'file_id': file.id, 'found': found, 'path_name': 'show_tabulation',
                               'button_name': 'view tabulation sheet'})
            else:
                return render(request, 'dashboard/tabulation/sheet_template.html',
                              {'found': found, 'path_name': '#'})

        context = get_context_data()
        return render(request, 'dashboard/tabulation/tabulation_filter.html', context)
    else:
        return render(request, 'post/404_page_all.html', {'message': "You don't have permission.",
                                                          'title': 'Permission denied '})


@login_required
def show_tabulation(request, pk):
    if request.user.is_admin:

        up_file = UploadResult.objects.get(pk=pk)

        res = Result.objects.filter(file=up_file)
        subjects = [sub for sub in res.first().storegrade_set.all()]

        context = {
            'up_file': up_file,
            'results': res,
            'subjects': subjects,
            'clg_name': settings.COLLEGE_NAME,
        }

        return render(request, 'dashboard/tabulation/tabulation.html', context)
    else:
        return render(request, 'post/404_page_all.html', {'message': "You don't have permission.",
                                                          'title': 'Permission denied '})


# view for mark sheet
@login_required
def mark_sheet_filter(request):

    """This view filters out and gets a id for result sheet file and
        sends the id as HttpResponse to frontend."""

    if request.user.is_admin:
        if request.method == 'POST':
            file = UploadResult.objects.filter(session=request.POST['session'], which_semester=request.POST['semester'],

                                               department=request.POST['department']).order_by('-session_year').first()
            found = False
            if file:
                found = True
                return render(request, 'dashboard/tabulation/sheet_template.html',
                              {'file_id': file.id, 'found': found, 'path_name': 'mark_sheets',
                               'button_name': 'view mark sheets'})
            else:
                return render(request, 'dashboard/tabulation/sheet_template.html',
                              {'found': found, 'path_name': '#'})
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission.",
                                                      'title': 'Permission denied '})


@login_required
def mark_sheets(request, pk):

    """This view renders all the marks sheets of specified result sheet file."""

    if request.user.is_admin:
        file = UploadResult.objects.get(pk=pk)
        return render(request, 'dashboard/tabulation/mark_sheet_filter.html', {'up_file': file})
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission.",
                                                      'title': 'Permission denied '})


@login_required
def get_tab_template_link(request):

    """This view plays a key role in navigation from one
        page to another without page refreshment using ajax.
        Mainly this view works on link based id's .
        When a particular id is encountered  desired page will
        be sent as HttpResponse to frontend/ajax."""

    if request.method == 'POST' and request.POST['link_id'] != '':
        link_id = request.POST['link_id']
        if link_id == '1':
            context = get_context_data()
            return render(request, 'dashboard/tabulation/tabulation_filter_full_template.html', context)

        if link_id == '2':
            context = get_context_data()
            return render(request, 'dashboard/tabulation/mark_sheet_filter_template.html', context)

        if link_id == '3':
            context = get_context_data()
            return render(request, 'dashboard/tabulation/short_mark_sheet.html', context)
        if link_id == '4':
            context = get_context_data()
            return render(request, 'dashboard/tabulation/search_to_edit_result_template.html', context)
    else:
        return False


def get_short_mark_sheet_filter(request):
    """This view filters out and gets a id for result sheet file and
            sends the id as HttpResponse to frontend."""

    if request.user.is_admin:
        if request.method == 'POST':
            file = UploadResult.objects.filter(session=request.POST['session'], which_semester=request.POST['semester'],

                                               department=request.POST['department']).order_by('-session_year').first()
            found = False
            if file:
                found = True
                return render(request, 'dashboard/tabulation/sheet_template.html',
                              {'file_id': file.id, 'found': found, 'path_name': 'get_short_mark_sheet',
                               'button_name': 'view short mark sheet'})
            else:
                return render(request, 'dashboard/tabulation/sheet_template.html',
                              {'found': found, 'path_name': '#'})
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission.",
                                                      'title': 'Permission denied '})


def get_short_mark_sheet(request, pk):
    """This view renders short form all the marks sheets of specified result sheet file."""

    if request.user.is_admin:
        file = UploadResult.objects.get(pk=pk)
        return render(request, 'dashboard/tabulation/short_mark_sheet_page.html', {'up_file': file})
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission.",
                                                      'title': 'Permission denied '})


# """ views for editing result """

def filter_result_to_edit(request):

    """Filters out result file for editing purpose."""

    if request.user.is_admin:

        file = UploadResult.objects.filter(session=request.POST['session'], which_semester=request.POST['semester'],

                                           department=request.POST['department']).order_by('-session_year').first()
        result = Result.objects.filter(file=file, roll=request.POST['roll']).first()
        found = False
        if file:
            found = True
            return render(request, 'dashboard/tabulation/sheet_template.html',
                          {'file_id': result.id, 'found': found, 'path_name': 'edit_result',
                           'button_name': 'Edit result'})
        else:
            return render(request, 'dashboard/tabulation/sheet_template.html',
                          {'found': found, 'path_name': '#'})
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission.",
                                                      'title': 'Permission denied '})


def edit_result(request, pk):

    """Renders all available subject to a specific student result
        and can select to edit from here."""

    if request.user.is_admin:

        result = Result.objects.get(pk=pk).storegrade_set.all()
        return render(request, 'dashboard/tabulation/edit_result_select_subject.html',
                      {'result': result,
                       'clg_name': settings.COLLEGE_NAME,})

    return render(request, 'post/404_page_all.html', {'message': "You don't have permission.",
                                                      'title': 'Permission denied '})


def edit_subject_mark(request, pk):

    """This view is responsible for editing  a subject mark .
        After editing it calls determine_grade function to calculate
        subject wise gpa and the calls determine_total_gpa_point to
        update old result data."""

    if request.user.is_admin:

        if request.POST:
            sub = StoreGrade.objects.get(pk=pk)
            total = sum(list(map(int, [request.POST['tca'], request.POST['tfe'], request.POST['pca'], request.POST['pfe']])))

            sub.s_t_c_asses_obt = int(request.POST['tca'])
            sub.s_t_f_exam_obt = int(request.POST['tfe'])
            sub.s_p_c_asses_obt = int(request.POST['pca'])
            sub.s_p_f_exam_obt = int(request.POST['pfe'])
            sub.mark = total
            sub.save()
            l_grade_grade_point = determine_grade(sub.subject.total_mark, sub.mark).split(',')
            sub.grade_chr = l_grade_grade_point[0]
            sub.grade_point = l_grade_grade_point[1]
            sub.save()
            determine_total_gpa_point(sub.result)

            return HttpResponse('<p style="color:black; text-align:center;">Update Successfully.</p>')

        sub = StoreGrade.objects.get(pk=pk)
        return render(request, 'dashboard/tabulation/edit_subject_mark.html',
                      {'sub': sub, 'clg_name': settings.COLLEGE_NAME,})

    return render(request, 'post/404_page_all.html', {'message': "You don't have permission.",
                                                      'title': 'Permission denied '})
