from .repositories.student_repository import StudentRepository
from .repositories.subject_repository import SubjectRepository
from .repositories.tutor_repository import TutorRepository
from .repositories.group_repository import GroupRepository
from .repositories.schedule_repository import ScheduleRepository
from .repositories.payment_repository import PaymentRepository
from .repositories.attendance_repository import AttendanceRepository
from .repositories.student_group_repository import StudentGroupRepository

class UnitOfWork:
    students = StudentRepository
    subjects = SubjectRepository
    tutors = TutorRepository
    groups = GroupRepository
    schedules = ScheduleRepository
    payments = PaymentRepository
    attendance = AttendanceRepository
    student_groups = StudentGroupRepository

 # Example script to demonstrate repository functionality
def demonstrate_repository_usage():
    # Перевірка, чи існує студент з таким email
    existing_student = UnitOfWork.students.model.objects.filter(email='davidalberg@icloud.com').first()
    if not existing_student:
        # Якщо студент не знайдений, додаємо його
        new_student = UnitOfWork.students.create(
            name='Maxim',
            surname='Oleh',
            birth_date='2008-10-01',
            email='maximoleh@icloud.com',
            phone_number='0686646754',
            status='Active'
        )
        print(f"New student added: {new_student}")
    else:
        print(f"Student with email {existing_student.email} already exists.")

    # Демонстрація вичитки всіх студентів
    all_students = UnitOfWork.students.all()
    print("All students:")
    for student in all_students:
        print(student)

    # Демонстрація вичитки студента за ID
    student_id = existing_student.id if existing_student else new_student.id
    fetched_student = UnitOfWork.students.get(student_id)
    print(f"Fetched student by ID ({student_id}): {fetched_student}")

demonstrate_repository_usage();