from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import Student, Attendance
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Home page view — shows different content based on login status
def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        else:
            return redirect('student_dashboard')
    return render(request, 'attendance_app/home.html')

# Redirect user based on role (you might not need this if using home as landing page)
def home_redirect(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        else:
            return redirect('student_dashboard')
    else:
        return redirect('login')

# User registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(user=user)  # Automatically create student profile
            login(request, user)
            return redirect('student_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'attendance_app/register.html', {'form': form})

# Student dashboard
@login_required
def student_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')

    student = get_object_or_404(Student, user=request.user)
    today = timezone.now().date()
    attendance, created = Attendance.objects.get_or_create(student=student, date=today)

    if request.method == 'POST':
        attendance.present = True
        attendance.save()
        return render(request, 'attendance_app/success.html')

    return render(request, 'attendance_app/dashboard.html', {'attendance': attendance})

# Admin dashboard
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    attendance_records = Attendance.objects.select_related('student').order_by('-date')
    return render(request, 'attendance_app/admin_dashboard.html', {'attendance_records': attendance_records})

# Custom login view (only needed if you're not using Django's auth_views.LoginView)
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_dashboard') if not user.is_staff else redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'attendance_app/login.html')

# Student logout — redirect to home
def student_logout(request):
    logout(request)
    return redirect('home')

# Admin logout — redirect to home
def admin_logout(request):
    logout(request)
    return redirect('home')
