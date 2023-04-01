from django.urls import path
from . import views
from . import views_for_registration_and_midterm_fee as v_f_r_m

"""Url paths for semester system"""

urlpatterns = [
    path('', views.semester_home, name='semester_home'),
    path('update-semester-fee/<int:pk>/', views.update_semester_fee, name='update_semester_fee'),

    path('registration/update-registration-fee/<int:pk>/', v_f_r_m.update_registration_fee, name='update_registration_fee'),
    path('registration/registration-home/', v_f_r_m.registration_home, name='registration_home'),

    path('midterm/update-midterm-fee/<int:pk>/', v_f_r_m.update_midterm_fee, name='update_midterm_fee'),
    path('midterm/midterm-home/', v_f_r_m.midterm_home, name='midterm_home'),
    path('college-private-links/update-midterm-fee-info/', v_f_r_m.update_midterm_info, name='update_midterm_info'),
    path('college-private-links/authenticate-admin-user/', v_f_r_m.authenticate_user_to_update_midterm_info,
         name='authenticate_admin_user_mid_term'),

    path('college-private-links/update-reg-fee-info/', v_f_r_m.update_registration_info, name='update_reg_info'),
    path('college-private-links/authenticate-admin-user-reg/', v_f_r_m.authenticate_user_to_update_registration_info,
         name='authenticate_admin_user_reg_fee'),

    path('college-private-links/refresh-add-prev-semester-data/', views.refresh_add_prev_s_data_form,
         name='refresh_add_prev_semester_data_form'),
    path('college-private-links/add-prev-semester-data/', views.add_prev_semester_data, name='add_prev_semester_data')

]