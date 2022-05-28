from django.urls import path
from . import views

urlpatterns = [
    path('', views.viewHome, name='home'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('register/', views.userRegister, name='register'),
    path('profile/', views.viewProfile, name='profile'),
    path('edit-profile/', views.editProfile, name='edit-profile'),
    path('tweets/', views.viewTweet, name='tweets'),
]