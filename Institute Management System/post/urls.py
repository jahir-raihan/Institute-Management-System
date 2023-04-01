from django.urls import path
from . import views

"""Url paths for post """

urlpatterns = [ 
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('<id>/view/', views.view, name='view'),
    path('<id>/update/', views.update, name='update'),
    path('<id>/delete/', views.delete, name='delete'),
    path('profile/<int:id>/', views.profile, name='profile'),

]
