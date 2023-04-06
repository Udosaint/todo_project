from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.APIRoutes.as_view(), name='api-route'),
    path('auth/register', views.ReisterView.as_view(), name='todo-register'),
    path('auth/login', views.LoginView.as_view(), name='todo-login'),
    path('auth/forget-password/<str:email>/', views.PasswordForgetView.as_view(), name='forget-password'),
    path('auth/reset-password', views.PasswordForgetView.as_view(), name='reset-password'),

    path('auth/verify', views.VerifyEmailView.as_view(), name='verify-email'),
    path('auth/resend/<str:id>', views.VerifyEmailView.as_view(), name='resend-email'), # to resend otp to user email

    path('todo/todos/', views.TodosView.as_view(), name='todos'),    
    path('todo/<str:id>/', views.TodoView.as_view(), name='view-todo'), # a particular todo task
    path('todo/task/<str:complete>/', views.CompletedTaskView.as_view(), name='complete-todo'), #complete todo task by user

    path('todo/user/profile/', views.ProfileView.as_view(), name='profile'),
    path('todo/profile/change-password/', views.ChangePasswordView.as_view(), name='change-password'),





]
