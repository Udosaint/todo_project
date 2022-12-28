from django.urls import path
from todo import views

urlpatterns = [
    path("", views.Index,  name="index"),
    path("test", views.test,  name="test"),
    path("register/", views.Signup,  name="register"),
    path("logout/", views.UserLogout,  name="logout"),


    path("todo/", views.Todos,  name="todo"),
    path("todo/add/", views.AddTodo,  name="add-todo"),
    path("todo/edit/<str:id>/", views.EditTodo,  name="edit-todo"),
    path("todo/delete/<str:id>/", views.DeleteTodo,  name="delete-todo"),
    path("todo/complete/<str:id>/", views.CompleteTodo,  name="complete-todo"),


    path("todo/profile/", views.Profile,  name="profile"),
    path("todo/edit-profile/", views.UpdateProfile,  name="edit-profile"),


    path("register-success/", views.RegisterSuccess,  name="register-success"),
    path("todo/verify-email/<str:token>", views.VerifyEmail,  name="verify-email"),
    path("verify-success/", views.VerifySuccess,  name="verify-success"),
]
