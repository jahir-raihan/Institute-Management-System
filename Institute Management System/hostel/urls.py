from django.urls import path
from . import views

"""Url paths for hostel System"""

urlpatterns = [
    path('', views.hostel_home, name='hostel_home'),
    path('search_to_add/', views.search_student_to_add, name='search-to-add'),
    path('view_student_details/<str:pk>/', views.view_student_details, name='view-student-details'),
    path('update-hotel-fee/<int:pk>/', views.update_hostel_fee, name='update_hostel_fee')
]