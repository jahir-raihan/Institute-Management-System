from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from collegeSystem.algorithms import get_session_year_list
import datetime

from dashboard.models import Transaction
from .forms import UserRegisterForm,  ProfileUpdateForm, TeacherRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Profile, StudentList
from .algoritms import send_code, confirm_code, give_role, give_special_permission, student_is_valid
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.conf import settings
from semesterSystem.models import SemesterSystem , SemesterSystemInfo

User = get_user_model()


def register(request):

    """View for registering a student at the beginning ."""
    session_year_list = sorted(get_session_year_list(datetime.datetime.now().year), reverse=True)
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            if student_is_valid(request.POST['roll'], request.POST['registration']):

                name = form.cleaned_data.get('name')
                fm = form.save()

                semester = SemesterSystem(student=fm)
                semester.save()
                semester_info = SemesterSystemInfo(semester_student=semester, amount_to_pay=settings.SEMESTER_FEE,
                                                   session=fm.session, department=fm.department,
                                                   semester=fm.semester)
                semester_info.save()
                pro = Profile.objects.create(image=request.FILES['image'], user=fm)
                pro.save()
                request.session['msg'] = f'Thank you {name}! Your account has been created!'
                request.session['success'] = True
                return redirect('login')
            else:
                return render(request, 'user/register.html', {'form': form, 'clg_name': settings.COLLEGE_NAME,
                                                              'session_year_list': session_year_list,
                                                              'error': f'Roll {form.cleaned_data.get("roll")} and '
                                                                       f'Registration {form.cleaned_data.get("registration")} not'
                                                                       f' found on our DataBase.', 'msg': True})
        else:
            form = UserRegisterForm()
            return render(request, 'user/register.html', {'form': form, 'clg_name': settings.COLLEGE_NAME,
                                                          'session_year_list': session_year_list,
                                                          'error': 'Provide valid Information.', 'msg':True})
    form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form, 'clg_name': settings.COLLEGE_NAME,
                                                  'session_year_list': session_year_list})


def login_user(request):

    """Login view """
    if request.method == 'POST':
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])

        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'user/login.html', {'msg': True,
                                                       'err': f"Account for {request.POST['email']} not found!"})
    return render(request, 'user/login.html')


@login_required
def logout_user(request):

    """Logs out a user"""

    logout(request)
    return redirect('login')


@login_required
def profile(request):

    """View for updating a user profile info."""

    if request.method == 'POST':

        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():

            p_form.save()
            messages.success(request, f'Your account has been Updated!')
            return redirect('profile')
    else:

        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {

        'p_form': p_form,
        'clg_name': settings.COLLEGE_NAME,
    }
    return render(request, 'users/profile.html', context)


# views for dashboard app
@login_required
def register_teacher_request(request):

    """This view receives a request for registering a new teacher.
        Send a auth code to the registering teacher email for email
        validation."""

    if request.method == 'POST' and request.user.is_admin:
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            send_code(form.cleaned_data.get('email'))
            context = {
                'form': form.cleaned_data,
                'email': form.cleaned_data.get('email'),
                'role': request.POST['role'],
                'clg_name': settings.COLLEGE_NAME,
            }
            return render(request, 'dashboard/confirm_code_template.html', context)
        return HttpResponse('<p style="color:#ff8800;text-align:center; margin:20% auto;'
                            '">Refresh the page and give valid data.</p>')
    return False


@login_required
def register_teacher(request):

    """If the auth code is valid , this view creates the teacher with
        desired roles given as choice in frontend."""

    if request.method == 'POST' and request.user.is_admin:
        form = TeacherRegistrationForm(request.POST)

        if form.is_valid():

            if confirm_code(request.POST['auth_code']):

                fm = form.save()

                give_role(fm, request.POST['role'])
                pro = Profile.objects.create(image=request.FILES['image'], user=fm)
                pro.save()
                return HttpResponse('<p style="color:rgb(44, 216, 44);text-align:center; height:200px;'
                                    ' margin-top:35%;">Created User Successfully</p>')
            return HttpResponse(
                '<p style="color:#ff8800;text-align:center; height:200px; margin-top:35%;">Authentication Failed!</p>')
        return HttpResponse(
            '<p style="color:#ff8800;text-align:center; height:200px; margin-top:35%;">Authentication Failed!</p>')

    return False


@login_required
def authenticate_admin_user(request):

    """This view authenticates if the requested user is admin or not
        before accessing the teacher registration form."""

    if request.method == 'POST' and request.user.is_admin:

        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
        if user and user.is_admin:
            return render(request, 'dashboard/teacher_creation_form_template.html',
                          {'clg_name': settings.COLLEGE_NAME,})
    return HttpResponse('<p style="color:rgb(255, 102, 42);'
                        ' text-align:center; height:200px; margin-top:35%;">Authentication Failed.</p>')


@login_required
def register_student(request):

    """Registering a student from dashboard System ."""
    if request.user.is_admin:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)

            if form.is_valid():
                if student_is_valid(request.POST['roll'], request.POST['registration']):
                    fm = form.save()
                    semester = SemesterSystem(student=fm)
                    semester.save()
                    semester_info = SemesterSystemInfo(semester_student=semester, amount_to_pay=settings.SEMESTER_FEE,
                                                       session=fm.session, department=fm.department,
                                                       semester=fm.semester)
                    s_perm = give_special_permission(fm, request.POST['discount'])
                    if s_perm:
                        semester_info.amount_to_pay = settings.SEMESTER_FEE // 2

                    semester_info.save()
                    pro = Profile.objects.create(image=request.FILES['image'], user=fm)
                    pro.save()

                    return HttpResponse('<p style="color:black;text-align:center; '
                                        'height:200px; margin-top:35%;">Created User Successfully</p>')

                return HttpResponse(f'<p style="color:black;text-align:center; margin:20% auto;">Roll "{request.POST["roll"]}" and Registration "{request.POST["registration"]}" not found in college Database. </p>')

            return HttpResponse('<p style="color:#ff8800;text-align:center; margin:20% auto;'
                                '">Refresh the page and give valid data.</p>')
    return False


def authenticate_admin_user_for_deafen_list(request):

    """This view authenticates admin user for uploading deafen list."""

    if request.method == 'POST' and request.user.is_admin:

        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
        if user and user.is_admin:
            return render(request, 'user/upload_deafen_list_auth_template.html', {'clg_name': settings.COLLEGE_NAME,})

    return HttpResponse('<p style="color:rgb(255, 102, 42);'
                        ' text-align:center; height:200px; margin-top:35%;">Authentication Failed.</p>')


def deafen_maker(request):

    """This view receives csv data for updating deafen student list.
        Deafen means those student's who has completed or quited diploma."""

    if request.user.is_admin:
        if request.method == 'POST' and request.FILES['file']:
            up_file = request.FILES['file']
            file_data = up_file.read().decode("utf-8")
            csv_data = file_data.split("\n")
            roll = csv_data.pop(0).split(',')
            for data in csv_data:
                student = User.objects.filter(roll=int(data)).first()
                if student is None:
                    continue
                student.is_deafen = True
                student.save()

            return HttpResponse('<p style="color:black;text-align:center; '
                                'height:200px; margin-top:35%;">Updated deafen list successfully.</p>')
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission to enter this page.",
                                                      'title': 'Permission denied'})


# views for uploading student list

def authenticate_admin_user_for_student_list(request):

    """This view authenticates admin user for uploading student list."""

    if request.method == 'POST' and request.user.is_admin:

        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
        if user and user.is_admin:
            return render(request, 'user/upload_student_list_auth_template.html', {'clg_name': settings.COLLEGE_NAME,})

    return HttpResponse('<p style="color:rgb(255, 102, 42);'
                        ' text-align:center; height:200px; margin-top:35%;">Authentication Failed.</p>')


def student_maker(request):

    """This view receives csv data for creating students in college data base .
        without uploading any student roll and registration list , no student will be able to
        register in website."""

    if request.user.is_admin:
        if request.method == 'POST' and request.FILES['file']:
            up_file = request.FILES['file']
            file_data = up_file.read().decode("utf-8")
            csv_data = file_data.split("\n")
            roll = csv_data.pop(0).split(',')
            for data in csv_data:
                roll_reg = data.split(',')
                student = StudentList(roll=roll_reg[0], registration=roll_reg[1].replace('\r', ''))
                student.save()

            return HttpResponse('<p style="color:black;text-align:center; '
                                'height:200px; margin-top:35%;">Uploaded student list successfully.</p>')
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission to enter this page.",
                                                      'title': 'Permission denied'})

#   views for searching transaction student perspective


def search_transaction_student_perspective(request):

    """This is view is made for student's only , student's
        can search through their transaction data by
        transaction receipt id."""

    if request.method == 'POST':

        r_id = request.POST['receipt_no']
        if r_id:
            data = Transaction.objects.filter(custom_receipt_id=int(r_id))
        else:
            data = Transaction.objects.order_by('custom_receipt_id').filter(recipient_student=request.user)
        return render(request, 'user/search_transaction_student_perspective_template.html',
                      {'transactions': data})
