from django.urls import path, include
from rest_framework import routers
from .views import (
    AttendanceViewSet, GroupViewSet, PaymentViewSet, ScheduleViewSet, StudentViewSet,
    StudentGroupViewSet, SubjectViewSet, TutorViewSet, LoginView, LogoutView, home,
    admin_dashboard, ChangePasswordView, student_list, student_details, group_list, add_student, student_groups_view,
    tutor_list, tutor_details, add_tutor
    # , student_add, teacher_list, teacher_add, lessons_list, lesson_add, group_list, group_add, attendance_list, attendance_add,payments_list, payment_add, schedule_list, schedule_add
)

router = routers.DefaultRouter()
router.register(r'attendance', AttendanceViewSet)
router.register(r'group', GroupViewSet)
router.register(r'payment', PaymentViewSet)
router.register(r'schedule', ScheduleViewSet)
router.register(r'student', StudentViewSet)
router.register(r'studentgroup', StudentGroupViewSet)
router.register(r'subject', SubjectViewSet)
router.register(r'tutor', TutorViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('api/', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('students/', student_list, name='student_list'),
   # path('student/<int:id>/', views.student_view, name='student_view'),
    path('student/<int:student_id>/details/', student_details, name='student_details'),
    path('student/add/', add_student, name='add_student'),
    path('student/<int:student_id>/groups/', student_groups_view, name='student_groups_view'),

    path('groups/', group_list, name='group_list'),
    path('tutors/', tutor_list, name='tutor_list'),
    path('tutor/<int:tutor_id>/', tutor_details, name='tutor_details'),
    path('tutor/add/', add_tutor, name='add_tutor'),

]
