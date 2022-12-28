from django.urls import path
from . import views

urlpatterns = [
    path('', views.APIRoutes.as_view(), name='api-route'),
    path('auth/register', views.ReisterView.as_view(), name='todo-register'),
    path('auth/login', views.LoginView.as_view(), name='todo-login'),

    path('todo/todos/', views.TodosView.as_view(), name='todos'),

    path('todo/profile/', views.ProfileView.as_view(), name='profile'),



    path('todo/<str:id>/', views.TodoView.as_view(), name='view-todo'),
]
