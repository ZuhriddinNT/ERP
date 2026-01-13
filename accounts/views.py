from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from .models import User
from courses.models import Course, Enrollment
from ratings.models import Rating


def login_view(request) :
    if request.user.is_authenticated :
        return redirect ( 'dashboard' )

    if request.method == 'POST' :
        username = request.POST.get ( 'username' )
        password = request.POST.get ( 'password' )
        user = authenticate ( request, username=username, password=password )

        if user is not None :
            login ( request, user )
            return redirect ( 'dashboard' )
        else :
            messages.error ( request, 'Invalid username or password' )

    return render ( request, 'accounts/login.html' )


def register_view(request) :
    if request.user.is_authenticated :
        return redirect ( 'dashboard' )

    if request.method == 'POST' :
        username = request.POST.get ( 'username' )
        email = request.POST.get ( 'email' )
        password = request.POST.get ( 'password' )
        password2 = request.POST.get ( 'password2' )
        user_type = request.POST.get ( 'user_type', 'student' )
        first_name = request.POST.get ( 'first_name' )
        last_name = request.POST.get ( 'last_name' )

        if password != password2 :
            messages.error ( request, 'Passwords do not match' )
        elif User.objects.filter ( username=username ).exists () :
            messages.error ( request, 'Username already exists' )
        elif User.objects.filter ( email=email ).exists () :
            messages.error ( request, 'Email already exists' )
        else :
            user = User.objects.create_user (
                username=username,
                email=email,
                password=password,
                user_type=user_type,
                first_name=first_name,
                last_name=last_name
            )
            login ( request, user )
            return redirect ( 'dashboard' )

    return render ( request, 'accounts/register.html' )


def logout_view(request) :
    logout ( request )
    return redirect ( 'home' )


@login_required
def dashboard(request) :
    user = request.user

    if user.is_admin_user :
        return admin_dashboard ( request )
    elif user.is_teacher :
        return teacher_dashboard ( request )
    else :
        return student_dashboard ( request )


def admin_dashboard(request) :
    total_users = User.objects.count ()
    total_students = User.objects.filter ( user_type='student' ).count ()
    total_teachers = User.objects.filter ( user_type='teacher' ).count ()
    total_courses = Course.objects.count ()
    active_courses = Course.objects.filter ( status='active' ).count ()
    total_enrollments = Enrollment.objects.count ()
    total_ratings = Rating.objects.count ()

    recent_users = User.objects.order_by ( '-date_joined' )[:5]
    recent_courses = Course.objects.order_by ( '-created_at' )[:5]
    recent_enrollments = Enrollment.objects.select_related ( 'student', 'course' ).order_by ( '-enrolled_at' )[:5]

    context = {
        'total_users' : total_users,
        'total_students' : total_students,
        'total_teachers' : total_teachers,
        'total_courses' : total_courses,
        'active_courses' : active_courses,
        'total_enrollments' : total_enrollments,
        'total_ratings' : total_ratings,
        'recent_users' : recent_users,
        'recent_courses' : recent_courses,
        'recent_enrollments' : recent_enrollments,
    }
    return render ( request, 'accounts/admin_dashboard.html', context )


def teacher_dashboard(request) :
    user = request.user
    courses = Course.objects.filter ( teacher=user )
    total_students = Enrollment.objects.filter ( course__teacher=user ).count ()

    ratings = Rating.objects.filter ( course__teacher=user )
    overall_rating = ratings.aggregate (
        avg_teaching=Avg ( 'teaching_quality' ),
        avg_content=Avg ( 'course_content' ),
        avg_communication=Avg ( 'communication' ),
        avg_helpfulness=Avg ( 'helpfulness' ),
        avg_punctuality=Avg ( 'punctuality' )
    )

    avg_metrics = [v for v in overall_rating.values () if v is not None]
    overall_avg = sum ( avg_metrics ) / len ( avg_metrics ) if avg_metrics else 0

    total_ratings = ratings.count ()
    active_courses = courses.filter ( status='active' ).count ()

    recent_feedback = Rating.objects.filter (
        course__teacher=user
    ).select_related ( 'student', 'course' ).order_by ( '-created_at' )[:5]

    context = {
        'courses' : courses,
        'total_students' : total_students,
        'overall_rating' : round ( overall_avg, 1 ),
        'total_ratings' : total_ratings,
        'active_courses' : active_courses,
        'recent_feedback' : recent_feedback,
        'rating_breakdown' : overall_rating,
    }
    return render ( request, 'accounts/teacher_dashboard.html', context )


def student_dashboard(request) :
    user = request.user
    enrollments = Enrollment.objects.filter ( student=user ).select_related ( 'course', 'course__teacher' )
    total_courses = enrollments.count ()

    ratings_given = Rating.objects.filter ( student=user ).count ()
    pending_ratings = enrollments.filter (
        ~Q ( course__id__in=Rating.objects.filter ( student=user ).values_list ( 'course_id', flat=True ) )
    ).count ()

    avg_progress = enrollments.aggregate ( Avg ( 'progress' ) )['progress__avg'] or 0
    certificates = enrollments.filter ( progress=100 ).count ()

    pending_rating_list = []
    for enrollment in enrollments :
        if not Rating.objects.filter ( student=user, course=enrollment.course ).exists () :
            pending_rating_list.append ( {
                'teacher' : enrollment.course.teacher,
                'course' : enrollment.course
            } )

    context = {
        'enrollments' : enrollments[:10],
        'total_courses' : total_courses,
        'ratings_given' : ratings_given,
        'pending_ratings' : pending_ratings,
        'avg_progress' : round ( avg_progress ),
        'certificates' : certificates,
        'pending_rating_list' : pending_rating_list[:4],
    }
    return render ( request, 'accounts/student_dashboard.html', context )


@login_required
def profile_view(request) :
    return render ( request, 'accounts/profile.html' )