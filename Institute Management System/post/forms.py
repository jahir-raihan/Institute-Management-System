from django import forms
from .models import Post


class PostCreateForm(forms.ModelForm):

    """Form for creating a post """

    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'date_posted']


class PostUpdateForm(forms.ModelForm):

    """Form for updating a post"""

    class Meta:
        model = Post
        fields = ['title', 'text', 'image']


