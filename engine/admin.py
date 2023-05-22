from django.contrib import admin
from .models import Student, Exam

# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'registration_number')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    pass