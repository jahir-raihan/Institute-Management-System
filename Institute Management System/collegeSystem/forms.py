from django import forms
from .models import ClassRoutine
from .models import UploadResult,  GetResult, ExamRoutine


class GetResultFormValidation(forms.ModelForm):
    class Meta:
        model = GetResult
        fields = ['roll', 'registration', 'semester']


class UploadResultForm(forms.ModelForm):

    """This form is for uploading result sheet """

    class Meta:
        model = UploadResult
        fields = ['exam', 'file', 'exam_year', 'session', 'started', 'ended',  'which_semester', 'department']


class UploadExamRoutine(forms.ModelForm):

    """This form is for uploading Exam routine pdf"""

    class Meta:
        model = ExamRoutine
        fields = ['file', 'semester', 'department']


class UploadClassRoutine(forms.ModelForm):

    """This form is for uploading Class routine pdf"""

    class Meta:
        model = ClassRoutine
        fields = ['file', 'semester', 'department']
