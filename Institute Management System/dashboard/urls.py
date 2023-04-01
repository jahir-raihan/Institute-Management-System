from django.urls import path
from . import views
from . import views_for_transaction
"""Url paths for dashboard system"""

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('college-user-system/', views.college_user_system, name='college_user_system'),
    path('get-link-template/', views.redirect_template_view, name='get_link_template'),
    path('hostel-system/', views.dashboard_hostel, name='dash_hostel'),
    path('authenticate-admin/', views.authenticate_to_update_semester_data , name='authenticate_admin'),
    path('authenticate-admin/update-semester/', views.update_semester, name='update_semester'),
    path('authenticate-admin-to-update-hostel-data/', views.authenticate_to_update_hostel_data,
         name='authenticate_admin_hostel'),
    path('authenticate-admin/update-hostel/', views.update_hostel, name='update_semester'),

    path('transaction/transaction-home/', views_for_transaction.transaction_home, name='transaction_home'),
    path('transaction/view-transaction/<str:trans_id>/', views_for_transaction.view_transaction, name='view_transaction'),
    path('transaction/get-link-template/', views_for_transaction.redirect_template_view, name='get_link_template'),



    path('transaction/get-extra-reason-template/',
         views_for_transaction.get_extra_reason_template, name='get_extra_reason'),


    path('transaction/create-custom-transaction/', views_for_transaction.make_custom_transaction, name='make_custom_trans'),
    path('transaction/transaction-history-student/<str:id>/', views_for_transaction.view_transaction_history_student,
         name='view_transaction_history_student'),

    #   url for tabulation sheet
    path('college-private-links/tabulation-sheet-filter/', views.tabulation_filter, name='tabulation_filter'),
    path('college-private-links/ekyd@fjsydk-kdf-djdfydh98@kdfkjdfnfjrckdwerkdfcpi-69039-adminuser-543joy567/'
         'tabulation-sheet/<str:pk>/', views.show_tabulation, name='show_tabulation'),

    path('college-private-links/mark-sheet-filter/', views.mark_sheet_filter, name='mark_sheet_filter'),
    path('college-private-links/a;ksdfhsdhfias@dkfjdifjdsff-dkfjk-adim-user-567'
         'joy677/get-all-mark-sheet/<str:pk>/', views.mark_sheets, name='mark_sheets'),
    path('college-private-links/get-template-link/', views.get_tab_template_link, name='get_tab_template_link'),

    path('college-private-links/short-mark-sheet-filter/', views.get_short_mark_sheet_filter,
         name='short_mark_sheet_filter'),
    path('college-private-links/fky@gidfidif-fijdfij$retrive-f-@async-9080dfidfjk-admin-user-543joy567/'
         'get-short-mark-sheet/<str:pk>/', views.get_short_mark_sheet, name='get_short_mark_sheet'),

    #  paths for editing result

    path('college-private-links/search-to-edit-result-sheet/', views.filter_result_to_edit, name='search_to_edit_result'),
    path('college-private-links/edit-result/<str:pk>/', views.edit_result, name='edit_result'),
    path('college-private-links/edit-subject-mark/<str:pk>/', views.edit_subject_mark, name='update_store_grade_info'),

    #  paths for statement section

    path('transaction/get-statement/', views_for_transaction.statement_filter, name='statement_filter'),
    path('transaction/<str:pk>/get_statement_data/', views_for_transaction.get_statement, name='get_statement_link'),
    path('transaction/query-student-arrears-data/', views_for_transaction.query_student_arrears_data,
         name='query_student_arrears_data'),
    path('transaction/get-transaction-statement-by-time-range-request/', views_for_transaction.get_trans_statement_by_time_range_request,
         name='get_trans_statement_by_time_range'),
    path('transaction/<str:pk>/get-transaction-statement/', views_for_transaction.get_transaction_statement,
         name='get-transaction-statement'),
    #  for transaction section
    path('transaction/refresh-c-trans/', views_for_transaction.refresh_c_trans, name='refresh_c_trans'),
]