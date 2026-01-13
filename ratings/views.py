from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Rating
from courses.models import Course, Enrollment

@login_required
def rate_teacher(request, course_id):
    if not request.user.is_student:
        messages.error(request, 'Only students can rate teachers')
        return redirect('dashboard')
    
    course = get_object_or_404(Course, id=course_id)
    
    # Check if student is enrolled
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.error(request, 'You must be enrolled in the course to rate it')
        return redirect('course_list')
    
    # Check if already rated
    existing_rating = Rating.objects.filter(student=request.user, course=course).first()
    
    if request.method == 'POST':
        teaching_quality = int(request.POST.get('teaching_quality'))
        course_content = int(request.POST.get('course_content'))
        communication = int(request.POST.get('communication'))
        helpfulness = int(request.POST.get('helpfulness'))
        punctuality = int(request.POST.get('punctuality'))
        comment = request.POST.get('comment', '')
        
        if existing_rating:
            # Update existing rating
            existing_rating.teaching_quality = teaching_quality
            existing_rating.course_content = course_content
            existing_rating.communication = communication
            existing_rating.helpfulness = helpfulness
            existing_rating.punctuality = punctuality
            existing_rating.comment = comment
            existing_rating.save()
            messages.success(request, 'Rating updated successfully')
        else:
            # Create new rating
            Rating.objects.create(
                student=request.user,
                course=course,
                teaching_quality=teaching_quality,
                course_content=course_content,
                communication=communication,
                helpfulness=helpfulness,
                punctuality=punctuality,
                comment=comment
            )
            messages.success(request, 'Rating submitted successfully')
        
        return redirect('dashboard')
    
    context = {
        'course': course,
        'existing_rating': existing_rating,
    }
    return render(request, 'ratings/rate_teacher.html', context)

@login_required
def my_ratings(request):
    if request.user.is_student:
        ratings = Rating.objects.filter(student=request.user).select_related('course', 'course__teacher')
    else:
        ratings = Rating.objects.filter(course__teacher=request.user).select_related('student', 'course')
    
    return render(request, 'ratings/my_ratings.html', {'ratings': ratings})
