from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from .models import Attendance, Group, Payment, Schedule, Student, StudentGroup, Subject, Tutor, Profile
from .serializers import AttendanceSerializer, GroupSerializer, PaymentSerializer, ScheduleSerializer, StudentSerializer, StudentGroupSerializer, SubjectSerializer, TutorSerializer
from .repositories.payment_repository import PaymentRepository
from django.urls import reverse
from django.contrib.auth.models import User


user = User.objects.get(username='superadmin')  # Змініть на свій логін
token, created = Token.objects.get_or_create(user=user)
print(token.key)

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def report(self, request):
        """
        Aggregated report of payments, including total amount paid and number of payments.
        """
        total_amount = PaymentRepository.get_total_amount_paid()
        total_payments = PaymentRepository.get_total_number_of_payments()
        report_data = {
            "total_amount_paid": total_amount,
            "total_number_of_payments": total_payments
        }
        return Response(report_data)

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class StudentGroupViewSet(viewsets.ModelViewSet):
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class LoginView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return render(request, 'tutor_app/login.html')  # Відображення сторінки логіну

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            profile = Profile.objects.get(user=user)
            if profile.role == 'student':
                return redirect('student_dashboard')
            elif profile.role == 'tutor':
                return redirect('tutor_dashboard')
            else:
                return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'tutor_app/login.html')

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)

def home(request):
    """
    Home page view that provides information about the center, reviews, contact details, and authentication options.
    """
    context = {
        'center_name': 'Tutor Center',
        'description': 'Welcome to Tutor Center! We offer professional tutoring services for students of all ages. Our experienced tutors are here to help you achieve your educational goals.',
        'reviews': [
            {'author': 'John Doe', 'content': 'Great experience! The tutors are very knowledgeable.'},
            {'author': 'Jane Smith', 'content': 'My child improved significantly in math after attending classes here.'},
        ],
        'contact': {
            'email': 'contact@tutorcenter.com',
            'phone': '+1234567890',
        }
    }
    return render(request, 'tutor_app/home.html', context)

from django.shortcuts import render

def login_view(request):
    return render(request, 'tutor_app/login.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.crypto import get_random_string
from tutor_app.models import Tutor, Student
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoginView(View):
    def get(self, request):
        return render(request, 'tutor_app/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'tutor_app/login.html')

class GenerateCredentialsView(View):
    def generate_credentials(self, user):
        username = f"{user.first_name}_{user.last_name}_{user.id}"
        password = user.date_of_birth.strftime("%d.%m.%Y")
        return username, password

    def post(self, request):
        users = Tutor.objects.all() | Student.objects.all()
        for user in users:
            if not user.user_account:
                username, password = self.generate_credentials(user)
                user_account = User.objects.create_user(username=username, password=password)
                user.user_account = user_account
                user.save()
        messages.success(request, 'User credentials have been generated successfully')
        return redirect('home')

@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    def get(self, request):
        return render(request, 'tutor_app/change_password.html')

    def post(self, request):
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        user = request.user

        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password changed successfully. Please use the new password the next time you log in.')
            return redirect('home')
        else:
            messages.error(request, 'Current password is incorrect.')
            return render(request, 'tutor_app/change_password.html')

class PasswordChangeRecommendationView(View):
    def get(self, request):
        messages.info(request, 'It is recommended that you change your password for security reasons.')
        return redirect('change_password')

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return Response(data)

class EditUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.email = request.data.get('email', user.email)
        user.save()
        return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)

@login_required
def admin_dashboard(request):
    return render(request, 'tutor_app/admin_dashboard.html')

# Student list view
def student_list(request):
    students = Student.objects.all()
    context = {
        'students': students,
    }
    return render(request, 'student_list.html', context)

# Student view
def student_view(request, id):
    student = get_object_or_404(Student, id=id)
    subjects = student.subjects.all()
    tutors = student.tutors.all()
    context = {
        'student': student,
        'subjects': subjects,
        'tutors': tutors,
    }
    return render(request, 'student_view.html', context)

# Student details view
def student_details(request, id):
    student = get_object_or_404(Student, id=id)
    context = {
        'student': student,
    }
    return render(request, 'student_details.html', context)

def student_list(request):
    students = Student.objects.all()
    return render(request, 'tutor_app/student_list.html', {'students': students})

def student_details(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'tutor_app/student_details.html', {'student': student})

def group_list(request):
    groups = Group.objects.prefetch_related('student_group_set__id_student', 'schedule_set__tutor_id')
    return render(request, 'tutor_app/group_list.html', {'groups': groups})


def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        date_of_birth = request.POST.get('date_of_birth')

        try:
            # Create new student instance
            student = Student(name=name, surname=surname, email=email, phone_number=phone_number,
                              birth_date=date_of_birth, status='Active')
            student.save()
            messages.success(request, 'Student added successfully!')
            return redirect(reverse('student_list'))
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect(reverse('add_student'))
    else:
        return render(request, 'tutor_app/add_student.html')


def student_groups_view(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student_groups = StudentGroup.objects.filter(id_student=student)

    context = {
        'student': student,
        'student_groups': student_groups,
    }
    return render(request, 'tutor_app/student_view.html', context)

def tutor_list(request):
    tutors = Tutor.objects.all()
    return render(request, 'tutor_app/tutor_list.html', {'tutors': tutors})


# View function for detailed information about a specific tutor
def tutor_details(request, tutor_id):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    groups = Group.objects.filter(schedule__tutor_id=tutor.id)
    return render(request, 'tutor_app/tutor_details.html', {'tutor': tutor, 'groups': groups})

def add_tutor(request):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        subject_id = request.POST['subject']
        salary_percentage = request.POST['salary_percentage']

        subject = Subject.objects.get(id=subject_id)

        Tutor.objects.create(
            name=name,
            surname=surname,
            email=email,
            phone_number=phone_number,
            subject=subject,
            salary_percentage=salary_percentage,
        )
        return redirect(reverse('tutor_list'))

    subjects = Subject.objects.all()
    return render(request, 'tutor_app/add_tutor.html', {'subjects': subjects})
