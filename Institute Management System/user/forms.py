from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

User = get_user_model()


class UserRegisterForm(UserCreationForm):

    """Form to register a student"""

    class Meta:
        model = User
        fields = ['email', 'name', 'mother', 'father', 'phone', 'roll', 'registration','session', 'semester', 'department', 'gender', 'religion', 'password1', 'password2']


class TeacherRegistrationForm(UserCreationForm):

    """Form to register a teacher"""

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'education', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):

    """Form to update a user profile picture.
        But we will never use it until needed."""

    class Meta:
        model = Profile
        fields = ['image']