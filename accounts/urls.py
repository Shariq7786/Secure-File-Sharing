from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('files/', views.user_files, name='user_files'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
