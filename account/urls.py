from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.news, name='news'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_detail, name='user_detail'),
    path('i_follow/', views.i_follow, name='i_follow'),
    path('edit_mypage/', views.edit_mypage, name='edit_mypage'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('confirm_delete_profile/', views.confirm_delete_profile, name='confirm_delete_profile'),
]

