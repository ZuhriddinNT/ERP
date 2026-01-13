from django.contrib import admin
from .models import Course, Enrollment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'code', 'teacher', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'code', 'teacher__username']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'progress', 'enrolled_at']
    list_filter = ['enrolled_at', 'course']
    search_fields = ['student__username', 'course__title']
