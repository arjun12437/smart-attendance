from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='attendance_app/login.html'), name='login'),
    path('logout/admin/', views.admin_logout, name='admin_logout'),
    path('logout/student/', views.student_logout, name='student_logout'),
]