from django.contrib import admin
from .models import User, Result
from .models import UploadResult, Semester,  ExamRoutine, ClassRoutine, Subjects, StoreGrade
# Register your models here.


class UploadResultAdmin(admin.ModelAdmin):
    list_display = ('which_semester', 'session_year', 'department')
    search_fields = ('session_year', 'which_semester')
    list_filter = ('session_year', 'which_semester')


class ResultSheetView(admin.ModelAdmin):
    list_filter = ('semester', 'student_name',)
    list_display = ('student_name', 'roll', 'grade_point', 'grade_char', 'semester')
    search_fields = ('roll', 'grade_char', 'grade_point', 'semester', 'date_added')
    filter_horizontal = ()
    ordering = ['semester', 'grade_char']


class StoreGradeView(admin.ModelAdmin):
    list_filter = ('subject', 'grade_point',)


    filter_horizontal = ()
    ordering = ['grade_point', 'grade_chr']


admin.site.register(UploadResult, UploadResultAdmin)
admin.site.register(Semester)
admin.site.register(Result, ResultSheetView)
admin.site.register(Subjects)
admin.site.register(StoreGrade, StoreGradeView)
admin.site.register(ClassRoutine)
admin.site.register(ExamRoutine)