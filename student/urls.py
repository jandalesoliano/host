from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("student/logout/", views.user_logout, name="user-logout"),
    path('result-page/', views.result_page, name='result-page'),
    path('view-recommended-courses/', views.recommended_courses, name='recommended_courses'),
]