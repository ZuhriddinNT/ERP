from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import Course, Enrollment
from ratings.models import Rating
from accounts.models import User


@login_required
def course_list(request) :
    if request.user.is_admin_user :
        courses = Course.objects.all ()
    elif request.user.is_teacher :
        courses = Course.objects.filter ( teacher=request.user )
    else :
        enrollments = Enrollment.objects.filter ( student=request.user )
        courses = Course.objects.filter ( enrollments__in=enrollments )

    return render ( request, 'courses/course_list.html', {'courses' : courses} )


@login_required
def course_detail(request, course_id) :
    course = get_object_or_404 ( Course, id=course_id )

    if request.user.is_student :
        enrollment = Enrollment.objects.filter ( student=request.user, course=course ).first ()
        if not enrollment :
            messages.error ( request, 'You are not enrolled in this course' )
            return redirect ( 'course_list' )
    elif request.user.is_teacher and course.teacher != request.user and not request.user.is_admin_user :
        messages.error ( request, 'You do not have access to this course' )
        return redirect ( 'course_list' )

    ratings = Rating.objects.filter ( course=course ).select_related ( 'student' )
    rating_stats = ratings.aggregate (
        avg_teaching=Avg ( 'teaching_quality' ),
        avg_content=Avg ( 'course_content' ),
        avg_communication=Avg ( 'communication' ),
        avg_helpfulness=Avg ( 'helpfulness' ),
        avg_punctuality=Avg ( 'punctuality' )
    )

    context = {
        'course' : course,
        'ratings' : ratings,
        'rating_stats' : rating_stats,
    }

    if request.user.is_student :
        context['enrollment'] = enrollment
        context['has_rated'] = Rating.objects.filter ( student=request.user, course=course ).exists ()

    return render ( request, 'courses/course_detail.html', context )


@login_required
def course_create(request) :
    if not request.user.is_admin_user :
        messages.error ( request, 'Only admins can create courses' )
        return redirect ( 'dashboard' )

    if request.method == 'POST' :
        title = request.POST.get ( 'title' )
        code = request.POST.get ( 'code' )
        description = request.POST.get ( 'description' )
        icon = request.POST.get ( 'icon', '📚' )
        teacher_id = request.POST.get ( 'teacher' )
        student_ids = request.POST.getlist ( 'students' )

        # Validate required fields
        if not all ( [title, code, teacher_id] ) :
            messages.error ( request, 'Please fill in all required fields' )
            teachers = User.objects.filter ( user_type='teacher' )
            students = User.objects.filter ( user_type='student' )
            return render ( request, 'courses/course_create.html', {
                'teachers' : teachers,
                'students' : students
            } )

        if Course.objects.filter ( code=code ).exists () :
            messages.error ( request, 'Course code already exists' )
        else :
            try :
                teacher = User.objects.get ( id=teacher_id, user_type='teacher' )
            except User.DoesNotExist :
                messages.error ( request, 'Selected teacher does not exist' )
                teachers = User.objects.filter ( user_type='teacher' )
                students = User.objects.filter ( user_type='student' )
                return render ( request, 'courses/course_create.html', {
                    'teachers' : teachers,
                    'students' : students
                } )

            course = Course.objects.create (
                title=title,
                code=code,
                description=description,
                teacher=teacher,
                icon=icon
            )

            # Enroll students
            enrolled_count = 0
            for student_id in student_ids :
                try :
                    if User.objects.filter ( id=student_id, user_type='student' ).exists () :
                        Enrollment.objects.create (
                            student_id=student_id,
                            course=course
                        )
                        enrolled_count += 1
                except Exception as e :
                    pass  # Skip invalid students

            messages.success ( request, f'Course created successfully with {enrolled_count} students enrolled' )
            return redirect ( 'course_detail', course_id=course.id )

    teachers = User.objects.filter ( user_type='teacher' )
    students = User.objects.filter ( user_type='student' )

    return render ( request, 'courses/course_create.html', {
        'teachers' : teachers,
        'students' : students
    } )


@login_required
def course_edit(request, course_id) :
    if not request.user.is_admin_user :
        messages.error ( request, 'Only admins can edit courses' )
        return redirect ( 'dashboard' )

    course = get_object_or_404 ( Course, id=course_id )

    if request.method == 'POST' :
        course.title = request.POST.get ( 'title' )
        course.code = request.POST.get ( 'code' )
        course.description = request.POST.get ( 'description' )
        course.icon = request.POST.get ( 'icon', '📚' )
        course.status = request.POST.get ( 'status' )
        teacher_id = request.POST.get ( 'teacher' )
        course.teacher_id = teacher_id
        course.save ()

        # Update enrollments
        student_ids = request.POST.getlist ( 'students' )
        current_enrollments = set ( course.enrollments.values_list ( 'student_id', flat=True ) )
        new_students = set ( int ( sid ) for sid in student_ids )

        # Remove unenrolled students
        to_remove = current_enrollments - new_students
        Enrollment.objects.filter ( course=course, student_id__in=to_remove ).delete ()

        # Add new students
        to_add = new_students - current_enrollments
        for student_id in to_add :
            Enrollment.objects.create ( student_id=student_id, course=course )

        messages.success ( request, 'Course updated successfully' )
        return redirect ( 'course_detail', course_id=course.id )

    teachers = User.objects.filter ( user_type='teacher' )
    students = User.objects.filter ( user_type='student' )
    enrolled_students = course.enrollments.values_list ( 'student_id', flat=True )

    return render ( request, 'courses/course_edit.html', {
        'course' : course,
        'teachers' : teachers,
        'students' : students,
        'enrolled_students' : list ( enrolled_students )
    } )


@login_required
def course_delete(request, course_id) :
    if not request.user.is_admin_user :
        messages.error ( request, 'Only admins can delete courses' )
        return redirect ( 'dashboard' )

    course = get_object_or_404 ( Course, id=course_id )

    if request.method == 'POST' :
        course_title = course.title
        course.delete ()
        messages.success ( request, f'Course "{course_title}" deleted successfully' )
        return redirect ( 'course_list' )

    return render ( request, 'courses/course_delete.html', {'course' : course} )
