import os
from datetime import datetime
from email.mime.image import MIMEImage

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import AuthCodes, StudentList
import random


#    This function will verify the code has been sent to the teacher email.
def confirm_code(code):

    """Confirms auth code that has been sent to registering teacher email.
        If the code matches it's returns True , else False."""

    try:
        get_code = AuthCodes.objects.get(code=int(code))

        get_code.delete()

        return True
    except:
        return False


#   this function sends a code the desired email .
def send_code(rec):

    """Function to send auth code for registering a new teacher in the system."""

    code = generate_code()  # here we are generating a new code for validation of the user.
    save_code = AuthCodes(code=code)
    save_code.save()

    # email alternative
    context = {

        "auth_code": code,
        'year': datetime.now().year,
        'clg_name': settings.COLLEGE_NAME,


    }
    html_content = render_to_string('emailTemplate/auth_code_email.html', context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        f"Authentication code",
        text_content,
        settings.EMAIL_HOST_USER,
        [rec, ]
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


#   Generating the code for verification
def generate_code():

    """Generating a random code for validation."""

    return random.randint(1, 999999)


#   script for giving role to registered  user

def give_role(user, role):

    """This function set's role for  registering teacher based on
        Choices given in frontend."""

    user.is_student = False
    if role == 'teacher':
        user.is_teacher = True
    elif role == 'accountant':
        user.is_accountant = True
    elif role == 'hostel_manager':
        user.is_hostel_super = True
    elif role == 'admin':
        user.is_admin = True
        user.is_hostel_manager = True

        user.is_staff = True
        user.is_teacher = True
        user.is_accountant = True
    user.save()


def give_special_permission(user, perm):

    """This function is for giving a special permission for
        half semester fee to particular students."""

    if perm == 'father_is_dead':
        user.father_is_dead = True
        user.save()
        return True
    elif perm == 'has_disability':
        user.has_disability = True
        user.save()
        return True
    elif perm == 'special_discount':
        user.special_discount = True
        user.save()
        return True
    else:
        return False


def student_is_valid(roll, registration):

    """Confirms if student is in college database or not."""

    try:
        student = StudentList.objects.get(roll=roll, registration=registration)
        return True
    except:
        return False
