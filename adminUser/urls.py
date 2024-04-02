from django.urls import path,include
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.home, name="login"),
    path('login', views.login, name ='loginners'),
    path("adminUser/", views.admin_dashboard, name="admin-dashboard"),
    path("adminUser/logout/", views.admin_logout, name="admin-logout"),
    path("student/logout/", views.user_logout, name="user-logout"),
    path('add-user/', views.add_user, name='add-user'),
    path("adminUser/handle-add-user/", views.handle_add_user, name="handle-add-user"),
    path('add-res/', views.add_res, name='add-res'),
    path('handle-add-res/', views.handle_add_res, name='handle-add-res'),
    ]
    