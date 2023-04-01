from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from hostel.algorithms import get_unpaid_hostel_students
from semesterSystem.algorithms import get_unpaid_semester_students
from semesterSystem.models import SemesterSystem, RegistrationFee, MidTermFee, SemesterSystemInfo
from hostel.models import HostelPaymentSystem, Hostel
from semesterSystem.models import MidTermFee, RegistrationFee, SemesterSystemInfo
from user.forms import UserRegisterForm
from collegeSystem.algorithms import get_session_year_list
from post.models import Notifications
from .models import Transaction, StatementHistory, TransactionStatementHistory
from django.db.models import Q
from .forms import ReasonSelectorForm
from django.contrib.auth.decorators import login_required
from collegeSystem.forms import UploadResultForm
from django.contrib.auth.decorators import login_required
from .algorithms import save_trans_reasons, determine_cash_in_cash_out, get_number_in_text, get_statement_data, \
    return_semester, get_all_fee_data, get_student_data, get_semester_in_word, calculate_total_mid_reg

import shortuuid
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from datetime import date, datetime

User = get_user_model()


def view_transaction(request, trans_id):

    """This view is responsible for showing a nice designed
        money receipt with real time transaction data."""

    try:
        rec = Transaction.objects.get(receipt_id=trans_id)
        rec_data = rec.transactiondetails_set.all()

        total = sum([i.transaction_amount for i in rec_data])
        num_in_text = get_number_in_text(total)
        context = {
            'rec': rec,
            'rec_data': rec_data,
            'total': total,
            'num_in_text': num_in_text,
            'clg_name': settings.COLLEGE_NAME,
        }
        for d in rec_data:
            var = str(d.transaction_reason).lower()
            z = var.replace(' ', '').replace('/', '').replace('.', '')
            if z.startswith('others('):
                context['other_reason'] = z.replace('others', '')
                z = 'others'

            context[z] = d.transaction_amount

        return render(request, 'dashboard/transaction/receipt.html', context)
    except Exception as e:

        return render(request, 'post/404_page_all.html', {'message': "No Such Transaction.",
                                                          'title': 'Not Found'})


@login_required
def transaction_home(request):

    """This is Home page view of Transaction system.
        Accountant and admin can view , search , or
        create a new transaction."""
    if request.user.is_accountant:

        notifications = Notifications.objects.order_by('-notification_date')[:10]
        if request.method == 'POST':
            key = request.POST['keyword']
            transactions = Transaction.objects.filter(
                Q(custom_receipt_id__startswith=key) | Q(recipient__startswith=key) | Q(student_roll__startswith=key)|
                Q(department__startswith=key) | Q(semester__startswith=key)
            )[:5]
            context = {
                'transactions': transactions,
                'clg_name': settings.COLLEGE_NAME,

            }
            return render(request, 'dashboard/transaction/transaction_home_template.html', context)

        transactions = Transaction.objects.order_by('-custom_receipt_id')[:5]
        form = ReasonSelectorForm()
        semester_department_form = UploadResultForm()
        session_year_list = sorted(get_session_year_list(datetime.now().year), reverse=True)
        form2 = UserRegisterForm()
        context = {
            'transactions': transactions,
            'form': form,
            'form2': form2,
            'semester_department_form': semester_department_form,
            'notifications': notifications,
            'time': timezone.now(),
            'clg_name': settings.COLLEGE_NAME,
            'session_year_list': session_year_list,
        }
        return render(request, 'dashboard/transaction/transaction_home.html', context)
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission to enter this page.",
                                                      'title': 'Permission Denied'})


@login_required
def transaction_history(request):
    if request.user.is_admin or request.user.is_accountant:
        transactions = Transaction.objects.order_by('custom_receipt_id')
        context = {
            'transactions': transactions,
            'clg_name': settings.COLLEGE_NAME,
        }
        return render(request, 'dashboard/transaction/transaction_history_template.html', context)
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission to enter this page.",
                                                      'title': 'Permission denied '})


@login_required
def redirect_template_view(request):

    """This view plays a key role in navigation from one
        page to another without page refreshment using ajax.
        Mainly this view works on link based id's .
        When a particular id is encountered  desired page will
        be sent as HttpResponse to frontend/ajax."""

    if request.method == 'POST' and request.POST['link_id'] != '':
        link_id = request.POST['link_id']
        if link_id == '1':
            transactions = Transaction.objects.order_by('-custom_receipt_id')[:5]
            context = {
                'transactions': transactions,
                'clg_name': settings.COLLEGE_NAME,
            }

            return render(request, 'dashboard/transaction/transaction_home_full_template.html', context)

        if link_id == '2':

            transactions = Transaction.objects.order_by('-date')[:50]

            context = {
                'transactions': transactions,
                'clg_name': settings.COLLEGE_NAME,
            }

            return render(request, 'dashboard/transaction/transaction_history_template.html', context)

        if link_id == '3':

            """This one returns a http response with the data
                of specified transaction data. """

            d = date.today()
            today_transactions = Transaction.objects.filter(date__year=d.year).filter(date__month=d.month).filter(date__day=d.day)
            this_month_transactions = Transaction.objects.filter(date__year=d.year,
                                                                 date__month=d.month)
            this_year_transactions = Transaction.objects.filter(date__year=d.year)

            last_five_year_transactions = Transaction.objects.filter(date__year__gte=d.year - 5)

            all_time_transactions = Transaction.objects.all()

            today = determine_cash_in_cash_out(today_transactions)

            this_month = determine_cash_in_cash_out(this_month_transactions)
            this_year = determine_cash_in_cash_out(this_year_transactions)
            last_five_year = determine_cash_in_cash_out(last_five_year_transactions)
            all_time = determine_cash_in_cash_out(all_time_transactions)

            context = {
                'today_in': today[0],
                'today_out': today[1],
                'this_month_in': this_month[0],
                'this_month_out': this_month[1],
                'this_year_in': this_year[0],
                'this_year_out': this_year[1],
                'last_five_year_in': last_five_year[0],
                'last_five_year_out': last_five_year[1],
                'all_time_in': all_time[0],
                'all_time_out': all_time[1],
                'clg_name': settings.COLLEGE_NAME,


            }
            return render(request, 'dashboard/transaction/transaction_database.html', context)

    else:
        return render(request, 'post/404_page_all.html', {'message': "Wrong path.",
                                                          'title': 'Not Found'})


def get_extra_reason_template(request):

    """View for generating new reason selector in custom transaction form"""

    if request.method == 'POST':
        form = ReasonSelectorForm()
        return render(request, 'dashboard/transaction/reason_selector_template.html', {'form': form})


@login_required
def make_custom_transaction(request):

    """View for saving a custom transaction in database with RDM management."""
    if request.user.is_accountant:
        if request.method == 'POST':
            r_id = shortuuid.ShortUUID().random(25)

            if request.POST['email'] == '':
                email = 'raihan.joy10@gmail.com'    # server data saving email
            else:
                email = request.POST['email']

            trans = Transaction(receipt_id=r_id, recipient=request.POST['recipient'],
                                signature_of_student=request.POST['recipient'],
                                signature_of_accountant=request.user.name,
                                email=email, transaction_type=request.POST['transaction_type'])

            if request.POST['roll']:
                student = User.objects.filter(roll=request.POST['roll']).first()
                if student:
                    trans.recipient_student = student
                    trans.recipient = student.name
                    trans.student_roll = student.roll
                    trans.department = student.department
                    trans.semester = student.semester
                    trans.signature_of_student = student.name
                    if request.POST['email'] == '':
                        trans.email = student.email
                    else:
                        trans.email = request.POST['email']

            trans.save()
            trans.custom_receipt_id = trans.id + 1000
            save_trans_reasons(trans, request.POST.getlist('transaction_reason'), request.POST.getlist('amount'),
                               request)
            return render(request, 'dashboard/transaction/view_receipt_btn_template.html', {'rec_id': r_id,
                                                                                            'clg_name': settings.COLLEGE_NAME,})
    return render(request, 'post/404_page_all.html', {'message': "You don't have permission to enter this page.",
                                                      'title': 'Permission denied '})


@login_required
def view_transaction_history_student(request, id):

    """This view returns transaction history of a student."""

    notifications = Notifications.objects.order_by('-notification_date')[:10]
    student = User.objects.get(pk=id)
    transactions = Transaction.objects.order_by('custom_receipt_id').filter(recipient_student=student).order_by('-date')
    context = {
        'transactions': transactions,
        'notifications': notifications,
        'time': timezone.now(),
        'clg_name': settings.COLLEGE_NAME,
    }
    return render(request, 'user/transaction_history_student.html', context)


#  views for  statements

def statement_filter(request):

    """Statement filter driver view , this view saves a history for filtering
        all type of fee data ."""

    if request.user.is_accountant:
        if request.method == 'POST':
            if request.POST['filter_type'] == '':
                return get_all_fee_data(request, request.POST, 'arrears_sheet')
            else:
                f_type = request.POST['filter_type']

                return get_statement_data(request, request.POST, f_type)

    return HttpResponse("Nothing here")


def get_statement_context(statement, data, title, to_pay):

    """We were repeating below while declaring context variable ,
        that's why i made this helper fuction to return context data."""

    context = {
        'data': data,
        'semester': return_semester(statement.semester),
        'session': statement.session,
        'department': statement.department,
        'title': title,
        'title1': statement.title,
        'f_type': statement.f_type,
        'to_pay': to_pay

    }
    return context


def get_statement(request, pk):

    """After the driver statement saves a filter history for filtering out ,
        this view generates the sheet."""

    if request.user.is_accountant:

        try:
            statement = StatementHistory.objects.get(pk=pk)
            if statement.f_type == 'Mid Term Fee':

                data = MidTermFee.objects.filter(session=statement.session, department=statement.department,
                                                 semester=statement.semester)
                title = "Mid Term fee statement of " + statement.department + return_semester(statement.semester) \
                        + 'semester' + ', session ' + statement.session
                to_pay = data[0].amount_to_pay
                context = get_statement_context(statement, data, title, to_pay)

            elif statement.f_type == 'Form Fill Up Fee':

                data = RegistrationFee.objects.filter(session=statement.session, department=statement.department,
                                                      semester=statement.semester)
                title = "Form Fill Up fee statement of " + statement.department + return_semester(statement.semester) \
                        + 'semester' + ', session ' + statement.session
                to_pay = data[0].amount_to_pay
                context = get_statement_context(statement, data, title, to_pay)

            elif statement.f_type == 'Semester Fee':

                data = SemesterSystemInfo.objects.filter(session=statement.session, department=statement.department,
                                                         semester=statement.semester)
                title = "Semester fee statement of " + statement.department + return_semester(statement.semester) \
                        + 'semester' + ', session ' + statement.session
                to_pay = settings.SEMESTER_FEE
                context = get_statement_context(statement, data, title, to_pay)

            elif statement.f_type == 'arrears_sheet':
                student_data = get_student_data(statement).datacontainerarrears_set.all().order_by('roll')
                get_semester = get_semester_in_word(statement.semester)

                context = {
                    'data': student_data,
                    'clg_name': settings.COLLEGE_NAME,
                    'clg_address': settings.CLG_ADDRESS,
                    'get_semester': get_semester,
                    'clg_code': settings.CLG_CODE,
                    'department': statement.department,
                    'session': statement.session,
                    'semester': return_semester(statement.semester),
                    's': statement.semester,
                    's1': statement.semester + 1
                }
                return render(request, 'dashboard/transaction/arrears_sheet.html', context)

            return render(request, 'dashboard/transaction/statement_of_fee.html', context)
        except:
            return HttpResponse("<p style='text-align:center; margin-top:35%; color:black;> "
                                "Something Went Wrong, Contact Developer.</p>")


def query_student_arrears_data(request):

    """This one is for querying through particular session and department
        students arrears data to show in custom transaction form left side ."""

    if request.user.is_accountant:
        if request.method == 'POST':
            try:
                student = User.objects.get(roll=request.POST['roll'])
                var = get_unpaid_semester_students(SemesterSystem)
                semester_data = SemesterSystem.objects.get(student=student)
                mid_term_data = calculate_total_mid_reg(MidTermFee.objects.filter(student=student, status='Unpaid'))
                form_fill_up_data = calculate_total_mid_reg(RegistrationFee.objects.filter(student=student,
                                                                                           status='Unpaid'))

                hostel_data = 0
                if student.in_hostel:
                    var = get_unpaid_hostel_students(Hostel)
                    hostel_data = Hostel.objects.get(student=student).amount_to_pay

                context = {
                    'semester_data': semester_data,
                    'mid_term_data': mid_term_data,
                    'form_fill_up_data': form_fill_up_data,
                    'hostel_data': hostel_data,
                    'student': student
                }
                return render(request, 'dashboard/transaction/query_student_arrears_template.html', context)

            except:
                pass


def refresh_c_trans(request):

    """Helper view function for refreshing custom transaction form in frontend."""

    transactions = Transaction.objects.order_by('-date')[:5]
    form = ReasonSelectorForm()
    semester_department_form = UploadResultForm()
    session_year_list = sorted(get_session_year_list(datetime.now().year), reverse=True)
    form2 = UserRegisterForm()
    context = {
        'transactions': transactions,
        'form': form,
        'form2': form2,
        'semester_department_form': semester_department_form,

        'time': timezone.now(),
        'clg_name': settings.COLLEGE_NAME,
        'session_year_list': session_year_list,
    }
    return render(request, 'dashboard/transaction/custom_transaction_refresh_template.html', context)

# for transaction statement section


def get_trans_statement_by_time_range_request(request):

    """Driver view for saving a filter history for generating transaction
        statement."""

    if request.user.is_accountant:
        if request.method == 'POST':
            time = request.POST['time_range']
            trans_statement = TransactionStatementHistory(time_range=time, generated_by=request.user)
            trans_statement.save()
            context = {
                'path_name': 'get-transaction-statement',
                'id': trans_statement.id,
                'found': True

            }

            return render(request, 'dashboard/transaction/transaction_statement_template.html', context)


def get_transaction_statement(request, pk):

    """Generates transactions statement."""

    if request.user.is_accountant:
        try:
            time = TransactionStatementHistory.objects.get(pk=pk).time_range
            d = date.today()
            
            """Two filters are not working for cpanel at here , i don't know why but i've marked it """
            
            if time == 'today':
                transactions = Transaction.objects.filter(
                    Q(date__year=d.year) & Q(date__month=d.month) & Q(date__day=d.day)
                )
            

            elif time == 'this_month':
                transactions = Transaction.objects.filter(
                    Q(date__year=d.year) & Q(date__month=d.month)
                )
                
            elif time == 'this_year':
                transactions = Transaction.objects.filter(date__year=d.year)

            elif time == 'last_five_years':
                transactions = Transaction.objects.filter(date__year__gte=d.year - 5)

            else:
                transactions = Transaction.objects.all()

            total_in_out = determine_cash_in_cash_out(transactions)

            context = {
                'data': transactions,
                'time_range': time,
                'total_cash_in': total_in_out[0],
                'total_cash_out': total_in_out[1],
                'datetime': d.today(),
                'generated_by': TransactionStatementHistory.objects.get(pk=pk).generated_by
            }
            return render(request, 'dashboard/transaction/transaction_statement.html', context)
        except:
            return HttpResponse("Something went wrong!")

    return render(request, 'post/404_page_all.html', {'message': "You don't have permission to enter this page.",
                                                      'title': 'Permission denied '})