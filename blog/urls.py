from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('create_post/', views.create_post, name='create-post'),
    path('edit/<int:post_id>/', views.update_post, name='update-post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete-post'),
    path('my-posts/', views.my_posts, name='my-posts'),
]