from django.contrib import admin
from .models import Student, Course, Lecturer

@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')  
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'student_count')  

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'Number of Students'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')  
    