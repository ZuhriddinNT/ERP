from django.urls import path
from . import views

urlpatterns = [
    path ( 'rate/<int:course_id>/', views.rate_teacher, name='rate_teacher' ),
    path ( 'my-ratings/', views.my_ratings, name='my_ratings' ),
]