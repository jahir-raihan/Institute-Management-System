from django.urls import path
from . import views

"""Url paths for college System"""

urlpatterns = [
    path('upload-result/', views.upload_result, name='upload_result'),
    path('<str:semester_url>/result/', views.view_results, name='view_results'),
    path('search-result/', views.view_results, name='view_result'),
    path('view-routine/', views.view_routine, name='view_routine'),
    path('view-class-routine/', views.view_class_routine, name='view_class_routine'),
    path('upload-routine/', views.upload_routine, name='upload_routine'),
    path('upload-class-routine/', views.upload_class_routine, name='upload_class_routine'),

    path('mark-sheet/<str:id>/', views.view_mark_sheet, name='view_mark_sheet')

]
