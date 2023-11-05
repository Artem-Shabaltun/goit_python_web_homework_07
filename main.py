from sqlalchemy import func, desc, select, and_

from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session


def select_01():
    """
    --- Знайти 5 студентів із найбільшим середнім балом з усіх предметів. ---
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student)\
        .join(Grade)\
        .group_by(Student.id)\
        .order_by(desc('average_grade'))\
        .limit(5)\
        .all()
    return result


def select_02():
    """
    --- Знайти студента із найвищим середнім балом з певного предмета. ---
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    where g.subject_id = 1
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 1;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade)\
        .join(Student)\
        .filter(Grade.subjects_id == 1)\
        .group_by(Student.id).order_by(desc('average_grade'))\
        .limit(1)\
        .all()
    return result

def select_03():

    """
    --- Знайти середній бал у групах з певного предмета. ---
    SELECT s.group_id, AVG(g.grade) AS average_grade
    FROM students s
    INNER JOIN grades g ON s.id = g.student_id
    INNER JOIN subjects sub ON g.subject_id = sub.id
    WHERE sub.id = 1 -- Замініть 1 на ID потрібного предмета
    GROUP BY s.group_id;
    """
    subject_id = 1

    result = session.query(Group.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Group) \
        .join(Student, Group.id == Student.group_id) \
        .join(Grade, Student.id == Grade.student_id) \
        .join(Subject, Grade.subjects_id == Subject.id) \
        .filter(Subject.id == subject_id) \
        .group_by(Group.name) \
        .order_by(Group.name) \
        .all()
    return result

def select_04():

    """
    --- Знайти середній бал на потоці (по всій таблиці оцінок). ---
    SELECT AVG(grade) AS average_grade
    FROM grades;
    """
    result = session.query(func.avg(Grade.grade).label('average_grade')).all()
    return result

def select_05():

    """
    --- Знайти які курси читає певний викладач. ---
    SELECT sub.name AS course_name
    FROM subjects sub
    INNER JOIN teachers t ON sub.teacher_id = t.id
    WHERE t.fullname = 'Jacqueline Davis' -- Замініть 'ПІБ викладача' на ім'я викладача, якого ви шукаєте
    """
    result = session.query(Subject.name) \
        .join(Teacher) \
        .filter(Teacher.fullname == 'Jacqueline Davis').all()
    return result

def select_06():

    """
    --- Знайти список студентів у певній групі. ---
    SELECT fullname
    FROM students
    WHERE group_id = 3; -- Замініть на ідентифікатор групи, яку ви шукаєте
    """
    result = session.query(Student.fullname) \
        .filter(Student.group_id == 3).all()
    return result

def select_07():

    """
    --- Знайти оцінки студентів у окремій групі з певного предмета. ---
    SELECT s.fullname AS student_name, g.grade, g.grade_date
    FROM students s
    JOIN grades g ON s.id = g.student_id
    JOIN subjects sub ON g.subject_id = sub.id
    WHERE s.group_id = 3 -- Замініть на ідентифікатор групи, яку ви шукаєте
      AND sub.id = 5; -- Замініть 1 на ID потрібного предмета

    """
    group_id = 3
    subject_id = 5

    result = session.query(Student.fullname, Grade.grade) \
        .join(Student, Grade.student_id == Student.id) \
        .join(Subject, Grade.subjects_id == subject_id) \
        .filter(Student.group_id == group_id, Subject.id == subject_id) \
        .all()

    return result

def select_08():

    """
    --- Знайти середній бал, який ставить певний викладач зі своїх предметів. ---
    SELECT t.fullname AS teacher_name, AVG(g.grade) AS average_grade
    FROM teachers t
    JOIN subjects sub ON t.id = sub.teacher_id
    JOIN grades g ON sub.id = g.subject_id
    GROUP BY t.fullname;
    """
    teacher_id = 3

    result = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .join(Subject, Grade.subjects_id == Subject.id) \
        .filter(Subject.teacher_id == teacher_id) \
        .scalar()

    return result

def select_09():

    """
    --- Знайти список курсів, які відвідує певний студент. ---
    SELECT sub.name AS course_name
    FROM students s
    JOIN grades g ON s.id = g.student_id
    JOIN subjects sub ON g.subject_id = sub.id
    WHERE s.fullname = 'Sarah Williams' -- Замініть 'ПІБ студента' на ім'я студента, якого ви шукаєте
    """
    result = session.query(Subject.name) \
        .join(Grade).join(Student) \
        .filter(Student.fullname == 'Michael Moore').all()
    return result

def select_10():

    """
    --- Список курсів, які певному студенту читає певний викладач. ---
    SELECT sub.name AS course_name
    FROM students s
    JOIN grades g ON s.id = g.student_id
    JOIN subjects sub ON g.subject_id = sub.id
    JOIN teachers t ON sub.teacher_id = t.id
    WHERE s.fullname = 'Michael Moore' -- Замініть 'ПІБ студента' на ім'я студента, якого ви шукаєте
      AND t.fullname = 'Jacqueline Davis' -- Замініть 'ПІБ викладача' на ім'я викладача, якого ви шукаєте
    """
    result = session.query(Subject.name) \
        .join(Teacher).join(Grade).join(Student) \
        .filter(Student.fullname == 'Michael Moore', Teacher.fullname == 'Jacqueline Davis').all()
    return result



def select_11():
    """
    --- Середній бал, який певний викладач ставить певному студентові. ---
    SELECT t.fullname AS teacher_name, s.fullname AS student_name, AVG(g.grade) AS average_grade
    FROM teachers t
    JOIN subjects sub ON t.id = sub.teacher_id
    JOIN grades g ON sub.id = g.subject_id
    JOIN students s ON g.student_id = s.id
    WHERE t.fullname = 'Jacqueline Davis' -- Замініть на ім'я викладача, якого ви шукаєте
      AND s.fullname = 'Michael Moore' -- Замініть на ім'я студента, якого ви шукаєте
    GROUP BY t.fullname, s.fullname;
  """
    result = session.query(
        Teacher.fullname.label('teacher_name'),
        Student.fullname.label('student_name'),
        func.avg(Grade.grade).label('average_grade')
    ).join(Subject, Teacher.id == Subject.teacher_id) \
        .join(Grade, Subject.id == Grade.subjects_id) \
        .join(Student, Grade.student_id == Student.id) \
        .filter(Teacher.fullname == 'Jacqueline Davis', Student.fullname == 'Michael Moore') \
        .group_by(Teacher.fullname, Student.fullname).all()
    return result

def select_12():
    """
    --- Оцінки студентів у певній групі з певного предмета на останньому занятті. ---
    select max(grade_date)
    from grades g
    join students s on s.id = g.student_id
    where g.subject_id = 2 and s.group_id  =3;

    select s.id, s.fullname, g.grade, g.grade_date
    from grades g
    join students s on g.student_id = s.id
    where g.subject_id = 2 and s.group_id = 3 and g.grade_date = (
        select max(grade_date)
        from grades g2
        join students s2 on s2.id=g2.student_id
        where g2.subject_id = 2 and s2.group_id = 3
    );
    :return:
    """

    subquery = (select(func.max(Grade.grade_date)).join(Student).filter(and_(
        Grade.subjects_id == 2, Student.group_id == 3
    ))).scalar_subquery()

    result = session.query(Student.id, Student.fullname, Grade.grade, Grade.grade_date) \
        .select_from(Grade) \
        .join(Student) \
        .filter(and_(Grade.subjects_id == 2, Student.group_id == 3, Grade.grade_date == subquery)).all()

    return result


if __name__ == '__main__':
    print("1)Знайти 5 студентів із найбільшим середнім балом з усіх предметів.")
    print(select_01())
    print("2)Знайти студента із найвищим середнім балом з певного предмета.")
    print(select_02())
    print("3)Знайти середній бал у групах з певного предмета.")
    print(select_03())
    print("4)Знайти середній бал на потоці (по всій таблиці оцінок).")
    print(select_04())
    print("5)Знайти які курси читає певний викладач.")
    print(select_05())
    print("6)Знайти список студентів у певній групі.")
    print(select_06())
    print("7)Знайти оцінки студентів у окремій групі з певного предмета.")
    print(select_07())
    print("8)Знайти середній бал, який ставить певний викладач зі своїх предметів.")
    print(select_08())
    print("9)Знайти список курсів, які відвідує певний студент.")
    print(select_09())
    print("10)Список курсів, які певному студенту читає певний викладач.")
    print(select_10())
    print("11)Середній бал, який певний викладач ставить певному студентові.")
    print(select_11())
    print("12)Оцінки студентів у певній групі з певного предмета на останньому занятті.")
    print(select_12())
