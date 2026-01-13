from django.contrib.auth.models import AbstractUser
from django.db import models


class User ( AbstractUser ) :
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )

    user_type = models.CharField ( max_length=10, choices=USER_TYPE_CHOICES, default='student' )
    phone = models.CharField ( max_length=20, blank=True, null=True )
    avatar = models.ImageField ( upload_to='avatars/', blank=True, null=True )
    bio = models.TextField ( blank=True, null=True )

    def __str__(self) :
        return f"{self.get_full_name () or self.username} ({self.user_type})"

    @property
    def is_student(self) :
        return self.user_type == 'student'

    @property
    def is_teacher(self) :
        return self.user_type == 'teacher'

    @property
    def is_admin_user(self) :
        return self.user_type == 'admin' or self.is_superuser