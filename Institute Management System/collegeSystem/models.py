from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

#   Getting the user model
User = get_user_model()


class Semester(models.Model):

    """This model is being used to list out semesters"""

    semester_name = models.CharField(max_length=50)

    def __str__(self):
        return self.semester_name


#   Choice sets for models Choice set


semester_choices = (
    (1, '1st semester'),
    (2, '2nd semester'),
    (3, '3rd semester'),
    (4, '4th semester'),
    (5, '5th semester'),
    (6, '6th semester'),
    (7, '7th semester')
)
semester_choices_result = (
    (1, '1st semester'),
    (2, '2nd semester'),
    (3, '3rd semester'),

)
department_choices = (
    ('Computer Science and Technology(85)', 'Computer Science and Technology(85)'),
    ('Computer Technology(66)', 'Computer Technology(66)'),
    ('Architecture and Interior Design Technology(87)', 'Architecture and Interior Design Technology(87)'),
    ('Civil Technology(64)', 'Civil Technology(64)'),
    ('Electrical  Technology(67)', 'Electrical  Technology(67)')
)

text_semester_choices = (
    ('FIRST SEMESTER EXAMINATION', 'FIRST SEMESTER EXAMINATION'),
    ('SECOND SEMESTER EXAMINATION', 'SECOND SEMESTER EXAMINATION'),
    ('THIRD SEMESTER EXAMINATION', 'THIRD SEMESTER EXAMINATION')
)


class Subjects(models.Model):
    """This is a helper model to determine the total mark of a subject.
        and how to calculate the grade ."""

    subject_code = models.CharField(max_length=20)
    subject_name = models.CharField(max_length=100)
    total_mark = models.IntegerField()
    subject_credit = models.IntegerField()
    total_mark_to_pass = models.IntegerField(default=0)
    #   for tabulation sheet
    s_t_t_c_asses = models.IntegerField(null=True, blank=True)
    s_t_t_f_exam = models.IntegerField(null=True, blank=True)
    s_p_t_c_asses = models.IntegerField(null=True, blank=True)
    s_p_t_f_exam = models.IntegerField(null=True, blank=True)

    sub_t_c_a_pass_mark = models.IntegerField(null=False, blank=True)
    sub_t_f_e_pass_mark = models.IntegerField(null=False, blank=True)
    sub_p_c_a_pass_mark = models.IntegerField(null=False, blank=True)
    sub_p_f_e_pass_mark = models.IntegerField(null=False, blank=True)

    def __str__(self):
        return f'{self.subject_name} ({self.subject_code})'


class ExamRoutine(models.Model):

    """This model is for uploading Exam routines """

    file = models.FileField(upload_to='routine_files')
    semester = models.IntegerField(choices=semester_choices)
    year = models.DateTimeField(default=timezone.now)
    department = models.CharField(max_length=100, choices=department_choices)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.year}  Exam routine'


class ClassRoutine(models.Model):

    """This model is for uploading Class routines"""

    file = models.FileField(upload_to='class_routine_files')
    semester = models.IntegerField(choices=semester_choices)
    department = models.CharField(max_length=100, choices=department_choices)
    year = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.year}  Class routine'


#   Below section will only contain Uploading and setting up Result System Models.

class UploadResult(models.Model):

    """This model is for Result System"""

    exam = models.CharField(max_length=150, choices=text_semester_choices)
    exam_year = models.CharField(max_length=30)
    started = models.DateField()
    ended = models.DateField()
    file = models.FileField(upload_to='results')
    which_semester = models.IntegerField(choices=semester_choices_result)
    department = models.CharField(max_length=100, choices=department_choices)
    session = models.CharField(max_length=30)

    session_year = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.session_year} {self.department} {self.which_semester} Result Sheet File of session {self.session} '


class Result(models.Model):

    """This model works along with UploadResult model .
        When a csv file being gets uploaded, this model
        stores the data of csv file along with student info"""

    student_name = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(UploadResult, on_delete=models.DO_NOTHING)
    roll = models.BigIntegerField()
    registration = models.BigIntegerField()
    grade_point = models.FloatField(default=0.00)
    grade_char = models.CharField(max_length=10)
    semester = models.IntegerField()

    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.student_name.name} result of semester {self.file.which_semester} department {self.file.department} , session {self.file.session}'


class StoreGrade(models.Model):

    """This model stores the data of each subject mark and grade obtained
        by a student From result sheet file."""

    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    mark = models.IntegerField()
    grade_chr = models.CharField(max_length=5)
    grade_point = models.CharField(default='0.00', max_length=4)
    subject_credit = models.IntegerField()

    #   for tabulation sheet.

    s_t_c_asses_obt = models.IntegerField(null=True, blank=True)
    s_t_f_exam_obt = models.IntegerField(null=True, blank=True)
    s_p_c_asses_obt = models.IntegerField(null=True, blank=True)
    s_p_f_exam_obt = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'Subject mark of {self.result} '


class GetResult(models.Model):

    """This model has been used as helper model for
        querying in result sheet for a student.
        Main purpose of this model is to give the
        ability to select semester and verify roll and
        registration number"""

    semester_choice = (
        (1, '1st semester'),
        (2, '2nd semester'),
        (3, '3rd semester')
    )
    roll = models.IntegerField()
    registration = models.BigIntegerField()
    semester = models.CharField(max_length=20, choices=semester_choice)


