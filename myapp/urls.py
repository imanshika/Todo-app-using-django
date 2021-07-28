from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path("", views.index, name='index'),
    path("search", views.search, name='search'),
    path("doneTodo/<int:id>/", views.doneTodo, name='doneTodo'),
    path("deleteTodo/<int:id>/", views.deleteTodo, name='deleteTodo'),
    path("editTodo/<int:id>/", views.editTodo, name='editTodo'),
    path("loginUser", views.loginUser, name='loginUser'),
    path("logoutUser", views.logoutUser, name='logoutUser'),
    path("signUp", views.signUp, name='signUp'),
    path("deleteAccount", views.deleteAccount, name='deleteAccount'),
    path("addTodo", views.addTodo, name='addTodo'),
    path("changePassword", views.changePassword, name='changePassword'),
]
