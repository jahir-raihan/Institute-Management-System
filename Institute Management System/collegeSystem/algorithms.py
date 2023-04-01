from .models import Result, StoreGrade, Subjects, UploadResult


def calculate_gpa(student, sub_codes, marks, semester, fs):

    """From calculating subject wise grades to total grade this is
        the parent function , who is responsible for all function
        call and saving data to database."""

    #  marks = list(map(int, marks)) commented because we don't need it anymore . any way we still need it.

    result = Result(student_name=student)
    result.roll = student.roll
    result.registration = student.registration
    result.semester = semester
    result.file = fs
    result.save()
    for i in range(len(sub_codes)):
        sub = get_subject_mark_credit(sub_codes[i])
        ex_mark = list(map(int, marks[i].split('-')))
        grade = determine_grade(sub.total_mark, sum(ex_mark)).split(',')

        store_grade_info = StoreGrade(result=result, subject=sub, mark=sum(ex_mark), grade_chr=grade[0],
                                      grade_point=grade[1], s_t_c_asses_obt=ex_mark[0], s_t_f_exam_obt=ex_mark[1],
                                      s_p_c_asses_obt=ex_mark[2], s_p_f_exam_obt=ex_mark[3],
                                      subject_credit=sub.subject_credit)
        store_grade_info.save()

    determine_total_gpa_point(result)


def determine_grade(total_mark, mark):

    """This function determines subject wise grade point and
        letter grade."""

    if total_mark == 200:
        return 'A+,4.00' if mark >= 160 else 'A,3.75' if mark >= 150 else 'A-,3.50' if mark >= 140 else 'B+,3.25' if mark >= 130 else 'B,3.00' if mark >= 120 else 'B-,2.75' if mark >= 110 else 'C+,2.50' if mark >= 100 else 'C,2.25' if mark >= 90 else 'D,2.00' if mark >= 80 else 'F,0.00'
    elif total_mark == 150:
        return 'A+,4.00' if mark >= 120 else 'A,3.75' if mark >= 112.5 else 'A-,3.50' if mark >= 105 else 'B+,3.25' if mark >= 97.5 else 'B,3.00' if mark >= 90 else 'B-,2.75' if mark >= 82.5 else 'C+,2.50' if mark >= 75 else 'C,2.25' if mark >= 67.5 else 'D,2.00' if mark >= 60 else 'F,0.00'
    elif total_mark == 100:
        return 'A+,4.00' if mark >= 80 else 'A,3.75' if mark >= 75 else 'A-,3.50' if mark >= 70 else 'B+,3.25' if mark >= 65 else 'B,3.00' if mark >= 60 else 'B-,2.75' if mark >= 55 else 'C+,2.50' if mark >= 45 else 'C,2.25' if mark >= 40 else 'D,2.00' if mark >= 35 else 'F,0.00'
    elif total_mark == 50:
        return 'A+,4.00' if mark >= 40 else 'A,3.75' if mark >= 37.5 else 'A-,3.50' if mark >= 35 else 'B+,3.25' if mark >= 32.5 else 'B,3.00' if mark >= 30 else 'B-,2.75' if mark >= 27.5 else 'C+,2.50' if mark >= 22.5 else 'C,2.25' if mark >= 20 else 'D,2.00' if mark >= 17.5 else 'F,0.00'


def get_subject_mark_credit(code):

    """This one returns a subject object by querying with subject code."""

    code = code.replace('\r', '')

    sub = Subjects.objects.get(subject_code=code)
    return sub  # [sub.total_mark, sub.subject_credit]


def determine_total_gpa_point(result):

    """This function calculates total grade point and grade letter by all subject marks."""

    total_credit = 0
    total_gpa = 0

    for g_data in result.storegrade_set.all():

        total_credit += g_data.subject_credit
        total_gpa += float(g_data.grade_point) * g_data.subject_credit

    gpa = round(total_gpa/total_credit, 2)
    result.grade_point = gpa
    result.grade_char = determine_gpa_chr(gpa)
    result.save()


def determine_gpa_chr(gpa):
    """This function determines the final grade of a result."""

    return 'A+' if gpa >= 4.00 else 'A' if gpa >= 3.75 else 'A-' if gpa >= 3.50 else 'B+' if gpa >= 3.25 else 'B' if gpa >= 3.00 else 'B-' if gpa >= 2.75 else 'C+' if gpa >= 2.50 else 'C' if gpa >= 2.25 else 'D' if gpa >= 2.00 else 'F'


def get_exam_year(year):

    """This function is also used to generate year list."""

    year_list = []
    for i in range(year-15, year + 1):
        year_list.append(i)
    return year_list


def get_session_year_list(year):

    """This function generates a year list dynamically."""

    year_list = []
    for i in range(year-10, year+2):
        year_list.append(f'{i-1}-{i}')
    return year_list


def has_validity(data):

    """This function checks if a result file already exist or not."""

    try:
        file = UploadResult.objects.get(exam=data['exam'], exam_year=data['exam_year'],
                                        which_semester=data['which_semester'], department=data['department'],
                                        session=data['session'])
        return False
    except:
        return True
