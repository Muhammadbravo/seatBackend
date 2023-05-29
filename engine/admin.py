from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'registration_number', "course")


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(ImageCourse)
class ImageAdmin(admin.ModelAdmin):
    pass

    def __str__(self):
        return f"ImageCourse: {self.image.name} ({self.image.content_type})"