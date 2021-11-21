from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('create/', views.image_create, name='create'),
    path('like/', views.image_like, name='like'),
    path('', views.image_list, name='list'),
    path('detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),
    path('styles/', views.styles, name='styles'),
    path('styles/<str:style>/', views.image_list, name='list_style'),
    path('edit_painting/<int:painting_id>/', views.edit_painting, name='edit_painting'),
    path('deactivate_painting/<int:painting_id>/', views.deactivate_painting, name='deactivate_painting'),
    path('activate_painting/<int:painting_id>/', views.activate_painting, name='activate_painting'),
    path('delete_painting/<int:painting_id>/', views.delete_painting, name='delete_painting'),
    path('confirm_delete_painting/<int:painting_id>/', views.confirm_delete_painting, name='confirm_delete_painting'),
    path('all_comments/<int:painting_id>/', views.all_comments, name='all_comments'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
