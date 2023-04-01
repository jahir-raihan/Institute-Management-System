from django.urls import path
from . import views

"""Url paths for User System"""

urlpatterns = [
    path('create-teacher-request/',
         views.register_teacher_request, name='register_teacher_request'),
    path('create-teacher/', views.register_teacher, name='register_teacher'),
    path('authenticate-admin-password/', views.authenticate_admin_user, name='authenticate_admin'),
    path('register-student/', views.register_student, name='register_student'),
    # path('authenticate-admin-password/', views.authenticate_admin_user, name='authenticate_admin'),
    # path('register-student/', views.register_student, name='register_student'),
    path('authenticate-admin-for-deafen-list/', views.authenticate_admin_user_for_deafen_list,
         name='authenticate_admin_for_deafen_list'),
    path('authenticate-admin-for-student-list/', views.authenticate_admin_user_for_student_list,
         name='authenticate_admin_for_student_list'),

    path('deafen-maker/', views.deafen_maker, name='deafen_maker'),
    path('student-maker/', views.student_maker, name='student_maker'),
    path('search-transaction-student/', views.search_transaction_student_perspective, name='search_transaction_student'),

]