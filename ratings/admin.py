from django.contrib import admin
from .models import Rating

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'average_rating', 'created_at']
    list_filter = ['created_at', 'course']
    search_fields = ['student__username', 'course__title', 'comment']
    readonly_fields = ['average_rating']
