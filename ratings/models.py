from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Rating(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_ratings')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='ratings')
    
    # Rating criteria (1-5 stars)
    teaching_quality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    course_content = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    communication = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    helpfulness = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    punctuality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    # Feedback
    comment = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"
    
    @property
    def average_rating(self):
        return round((
            self.teaching_quality +
            self.course_content +
            self.communication +
            self.helpfulness +
            self.punctuality
        ) / 5, 1)
