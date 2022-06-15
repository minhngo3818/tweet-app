from django.urls import path
from . import views

urlpatterns = [
    path('', views.viewHome, name='home'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('register/', views.userRegister, name='register'),

    path('profile/', views.viewProfile, name='profile'),
    path('other-profile/<str:pk>/', views.viewOtherProfile, name='other-profile'),
    path('edit-profile/', views.editProfile, name='edit-profile'),

    path('tweets/', views.viewTweets, name='tweets'),
    path('like/', views.likedTweet, name='like-tweet'),
    path('edit-tweet/<str:pk>/', views.editMyTweet, name='edit-tweet'),
    path('delete-tweet/<str:pk>/', views.deleteMyTweet, name='delete-tweet'),

    path('comment-tweet/<str:pk>/', views.commentTweet, name='comment-tweet'),
    path('like-comment/<str:pk>/', views.likeComment, name='like-comment'),
    path('edit-comment/<str:pk>/', views.editComment, name='edit-comment'),
    path('delete-comment/<str:pk>/', views.deleteComment, name='delete-comment'),
    path('reply-comment/<str:pk>/', views.replyComment, name='reply-comment')    
]