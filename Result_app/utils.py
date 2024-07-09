def GPA_ENGINE(course_results):
    total_point_list = []
    course_total_unit_list = []

    for result in course_results:
        # print(result.course.credit)
        # print(result.total_point)
        course_total_unit_list.append(result.course.credit)
        total_point_list.append(result.total_point)

    # int_total_unit = list(map(int, total_point_list))
    # int_credit_unit = list(map(int, course_total_unit_list))

    total_point = sum(total_point_list)
    course_total_unit = sum(course_total_unit_list)

    # print('Course_List: ', course_total_unit_list)
    # print('total_point_List: ', total_point_list)
    # print('Total_Unit: ', total_point)
    # print('Total_Credit_Unit: ', course_total_unit)

    gpa = total_point/course_total_unit
    return round(gpa, 2)


def grade_eng(score):
    sore = []
    if 70 <= int(score) <= 100:
        letter_grade = 'A'
        grade_point = 5
        sore.append(letter_grade)
        sore.append(grade_point)

    elif 60 <= int(score) <= 69:
        letter_grade = 'B'
        grade_point = 4
        sore.append(letter_grade)
        sore.append(grade_point)

    elif 50 <= int(score) <= 59:
        letter_grade = 'C'
        grade_point = 3
        sore.append(letter_grade)
        sore.append(grade_point)

    elif 45 <= int(score) <= 49:
        letter_grade = 'D'
        grade_point = 2
        sore.append(letter_grade)
        sore.append(grade_point)

    elif 40 <= int(score) <= 44:
        letter_grade = 'E'
        grade_point = 1
        sore.append(letter_grade)
        sore.append(grade_point)

    else:
        letter_grade = 'F'
        grade_point = 0
        sore.append(letter_grade)
        sore.append(grade_point)

    return sore

