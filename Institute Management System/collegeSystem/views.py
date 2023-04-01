import os
from email.mime.image import MIMEImage
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


from .models import ClassRoutine
from datetime import datetime

from .forms import UploadClassRoutine
from .models import User, UploadResult, Result,   ExamRoutine
from .forms import UploadResultForm,  GetResultFormValidation, UploadExamRoutine
from django.core import serializers
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils import timezone
from post.models import Notifications
from .algorithms import calculate_gpa, get_exam_year, get_session_year_list, has_validity


# """end upload grade view"""

# """view_result view"""


@login_required
def view_results(request):

    """This view returns query data of result sheet for particular
        Student ."""

    notifications = Notifications.objects.order_by('-notification_date')[:10]
    form = GetResultFormValidation()
    if request.method == 'POST':

        if request.POST['roll'] == '' or request.POST['registration'] == '':
            return HttpResponse('<p style="color:#ff8800;text-align:center; margin-bottom:20%;'
                                '">Refresh the page and give valid inputs.</p>')
        result = Result.objects.filter(roll=request.POST['roll'], registration=request.POST['registration'],
                                       semester=request.POST['semester']).first()

        if result:
            context = {
                'result': result,

            }

            return render(request, 'collegeSystem/show_result_template.html', context)
        else:
            return HttpResponse("<p style='text-align:center; color:black; padding:1em 0;'>Not Found!</p>")

    context = {
        'form': form,
        'notifications': notifications,
        'time': timezone.now(),
        'clg_name': settings.COLLEGE_NAME,
    }

    return render(request, 'collegeSystem/result.html', context)


# """end view_result view"""

# view mark sheet

@login_required
def view_mark_sheet(request, id):
    try:
        result = Result.objects.get(pk=id)
        mark_sheet = result.storegrade_set.all()
        # printing size from top 51 mm , rest are 0 .
        context = {

            'result': result,
            'mark_sheet': mark_sheet,
        }
        return render(request, 'collegeSystem/grade.html', context)
    except Exception as e:
        return render(request, 'post/404_page_all.html', {'message': "No such mark sheet.",
                                                          'title': 'Not Found'})

# end view mark sheet


# """upload result view"""
@login_required
def upload_result(request):

    """This view is used for uploading result sheet file.
        Saving the file to database and setting up the result
        sheet data to students result data as per details."""

    year_list = reversed(get_exam_year(datetime.now().year))
    session_year_list = sorted(get_session_year_list(datetime.now().year), reverse=True)
    notifications = Notifications.objects.order_by('-notification_date')[:10]
    msg = False
    if request.user.is_admin:
        if request.method == 'POST':

            if has_validity(request.POST):
                form = UploadResultForm(request.POST, request.FILES)

                if form.is_valid():
                    up_file = request.FILES['file']
                    file_data = up_file.read().decode("utf-8")
                    csv_data = file_data.split("\n")
                    roll_sub_codes = csv_data.pop(0).split(',')[1:]

                    fs = form.save()
                    users = []
                    for data in csv_data:
                        """Tabulation sheet work will start from here"""

                        d = data.split(',')
                        student_roll = d.pop(0)

                        student = User.objects.filter(roll=int(student_roll)).first()

                        if student is None:
                            continue
                        users.append(student)
                        calculate_gpa(student, roll_sub_codes, d, form.cleaned_data.get('which_semester'), fs)
                    users_emails = [user.email for user in users]

                    # email alternatives
                    context = {
                        'year': datetime.now().year,
                        'domain': request.META['HTTP_HOST'],
                        'clg_name': settings.COLLEGE_NAME,
                        "result_title": fs.exam,


                    }

                    html_content = render_to_string('emailTemplate/result_email.html', context)
                    text_content = strip_tags(html_content)

                    email = EmailMultiAlternatives(
                        f"{fs.exam} RESULT HAS BEEN PUBLISHED.",

                        text_content,
                        settings.EMAIL_HOST_USER,
                        users_emails,

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
                    # end email alternatives
            msg = True

        form = UploadResultForm()
        context = {
            'form': form,
            'notifications': notifications,
            'time': timezone.now(),
            'year_list': year_list,
            'session_year_list': session_year_list,
            'clg_name': settings.COLLEGE_NAME,
            'msg': msg,
        }
        return render(request, 'collegeSystem/upload_result.html', context)
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission.",
                                                      'title': 'Permission denied'})
# """end upload result view"""

# """upload exam routine view"""


@login_required
def upload_routine(request):

    """This view is for uploading routine """
    notifications = Notifications.objects.order_by('-notification_date')[:10]
    default_form = UploadExamRoutine()
    if request.user.is_admin or request.user.is_staff:
        if request.method == 'POST':
            form = UploadExamRoutine(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                # email alternatives
                users_emails = [user.email for user in User.objects.filter(semester=form.cleaned_data.get('semester')).filter(department=form.cleaned_data.get('department'))]

                context = {

                    "routine_title": "Exam routine has been published.",
                    "routine_department": form.cleaned_data.get('department'),
                    "routine_semester": form.cleaned_data.get('semester'),
                    'url': 'view-routine',
                    'domain': request.META['HTTP_HOST']

                }
                html_content = render_to_string('emailTemplate/routine_email.html', context)
                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                    f"Exam routine has been published.",
                    text_content,
                    settings.EMAIL_HOST_USER,
                    users_emails
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
                # end email alternatives
                return render(request, 'collegeSystem/upload_routine.html', {'form': default_form,
                                                                             'clg_name': settings.COLLEGE_NAME,})

        context = {
            'form': default_form,
            'notifications': notifications,
            'time': timezone.now(),
            'clg_name': settings.COLLEGE_NAME,
        }
        return render(request, 'collegeSystem/upload_routine.html', context)
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission.",
                                                      'title': 'Permission denied '})

# """end upload exam routine view"""


# upload class routine view

def upload_class_routine(request):

    """This view is for uploading routine """
    notifications = Notifications.objects.order_by('-notification_date')[:10]
    default_form = UploadClassRoutine()
    if request.user.is_admin or request.user.is_staff:
        if request.method == 'POST':

            form = UploadClassRoutine(request.POST, request.FILES)
            if form.is_valid():
                form.save()

                # email alternatives

                users_emails = [user.email for user in User.objects.filter(
                    semester=form.cleaned_data.get('semester')).filter(department=form.cleaned_data.get('department'))]

                context = {

                    "routine_title": "Class routine has been published.",
                    "routine_department": form.cleaned_data.get('department'),
                    "routine_semester": form.cleaned_data.get('semester'),
                    "url": 'view-class-routine',
                    'domain': request.META['HTTP_HOST']

                }
                html_content = render_to_string('emailTemplate/routine_email.html', context)
                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                    f"Class routine has been published.",
                    text_content,
                    settings.EMAIL_HOST_USER,
                    users_emails
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
                # end email alternatives
                return render(request, 'collegeSystem/upload_class_routine.html', {'form': default_form,
                                                                                   'clg_name': settings.COLLEGE_NAME,})

        context = {
            'form': default_form,
            'notifications': notifications,
            'time': timezone.now(),
            'clg_name': settings.COLLEGE_NAME,
        }
        return render(request, 'collegeSystem/upload_class_routine.html', context)
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission.",
                                                      'title': 'Permission denied '})

# end upload class routine view

# """view_routine view"""


@login_required
def view_routine(request):

    """This view query's  a particular Exam routine
        and returns it to end user."""
    notifications = Notifications.objects.order_by('-notification_date')[:10]
    form = UploadExamRoutine()
    if request.method == 'POST':
        file = ExamRoutine.objects.filter(semester=request.POST['semester']).filter(department=request.POST['department']).order_by('-date_posted').first()

        return render(request, 'collegeSystem/view_routine_template.html', {'file': file, 'notifications': notifications, 'time': timezone.now()})
    return render(request, 'collegeSystem/view_exam_routine.html', {'form': form, 'notifications': notifications, 'time': timezone.now(),
                                                                    'clg_name': settings.COLLEGE_NAME,})

# """end view_routine view"""

# """class_routine view"""


@login_required
def view_class_routine(request):

    """This view query's  a particular Class routine
        and returns it to end user."""
    notifications = Notifications.objects.order_by('-notification_date')[:10]
    form = UploadClassRoutine()
    if request.method == 'POST':
        try:
            file = ClassRoutine.objects.filter(semester=request.POST['semester']).filter(
                    department=request.POST['department']).order_by('-year').first()
        except:
            file = ''

        return render(request, 'collegeSystem/view_routine_template.html', {'file': file, 'notifications': notifications,
                                                                            'time': timezone.now()})
    return render(request, 'collegeSystem/view_class_routine.html', {'form': form, 'notifications': notifications,'time': timezone.now(),
                                                                     'clg_name': settings.COLLEGE_NAME,})

# """end class_routine view"""
# Create your views here.
