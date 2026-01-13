from django.db import models
from django.conf import settings


class Course ( models.Model ) :
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('completed', 'Completed'),
    )

    title = models.CharField ( max_length=200 )
    code = models.CharField ( max_length=20, unique=True )
    description = models.TextField ()
    teacher = models.ForeignKey ( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='taught_courses' )
    status = models.CharField ( max_length=20, choices=STATUS_CHOICES, default='active' )
    icon = models.CharField ( max_length=50, default='📚' )
    created_at = models.DateTimeField ( auto_now_add=True )
    updated_at = models.DateTimeField ( auto_now=True )

    class Meta :
        ordering = ['-created_at']

    def __str__(self) :
        return f"{self.title} ({self.code})"

    @property
    def student_count(self) :
        return self.enrollments.count ()

    @property
    def average_rating(self) :
        from ratings.models import Rating
        ratings = Rating.objects.filter ( course=self )
        if not ratings.exists () :
            return 0

        avg = ratings.aggregate (
            avg_teaching=models.Avg ( 'teaching_quality' ),
            avg_content=models.Avg ( 'course_content' ),
            avg_communication=models.Avg ( 'communication' ),
            avg_helpfulness=models.Avg ( 'helpfulness' ),
            avg_punctuality=models.Avg ( 'punctuality' )
        )

        values = [v for v in avg.values () if v is not None]
        return round ( sum ( values ) / len ( values ), 1 ) if values else 0


class Enrollment ( models.Model ) :
    student = models.ForeignKey ( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments' )
    course = models.ForeignKey ( Course, on_delete=models.CASCADE, related_name='enrollments' )
    enrolled_at = models.DateTimeField ( auto_now_add=True )
    progress = models.IntegerField ( default=0 )

    class Meta :
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']

    def __str__(self) :
        return f"{self.student.username} - {self.course.title}"