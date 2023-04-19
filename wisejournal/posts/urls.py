from django.urls import path

from . import views

urlpatterns = [
    # Main page
    path("", views.index, name="index"),
    # Group page
    path('group/<slug:slug>/', views.group_posts, name='group'),
    # Add new post
    path('new/', views.new_post, name='new_post'),
    # Following page
    path('follow/', views.follow_index, name='follow_index'),
    # Follow user
    path('<str:username>/follow', views.profile_follow, name='profile_follow'),
    # Unfollow user
    path('<str:username>/unfollow', views.profile_unfollow, name='profile_unfollow'),
    # Profile page
    path('<str:username>/', views.profile, name='profile'),
    # Post view page
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    # Post edit page
    path('<str:username>/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    # Comments for post
    path("<str:username>/<int:post_id>/comment/", views.add_comment, name="add_comment"),
]
