from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {'Present' if self.present else 'Absent'}"
