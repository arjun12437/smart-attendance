from django.contrib import admin
from .models import Student, Attendance

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Show associated user in admin list

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'present')  # Show key fields
    list_filter = ('date', 'present')              # Add sidebar filters
    search_fields = ('student__user__username',)   # Allow search by username
