# Django Library
from django.urls import path

# Local Imports
from . import views

# Namespace - blog.
app_name = 'blog'

# List of blog pages' addresses.
urlpatterns = [
    # Homepage
    path('', views.PostListView.as_view(), name='index'),
    # Profile related pages
    path(
        'profile/edit/',
        views.UpdateUserProfile.as_view(),
        name='edit_profile',
    ),
    path(
        'profile/<slug:username>/',
        views.ShowUserProfile.as_view(),
        name='profile',
    ),
    # Post related pages
    path(
        'posts/<int:pk>/',
        views.PostDetailView.as_view(),
        name='post_detail',
    ),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path(
        'posts/<int:pk>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post',
    ),
    path(
        'posts/<int:pk>/edit/',
        views.PostEditView.as_view(),
        name='edit_post',
    ),
    # Comments to post pages
    path(
        'posts/<int:pk>/comment/',
        views.AddComment.as_view(),
        name='add_comment',
    ),
    path(
        'posts/<int:pk>/edit_comment/<int:comment_id>/',
        views.EditComment.as_view(),
        name='edit_comment',
    ),
    path(
        'posts/<int:pk>/delete_comment/<int:comment_id>/',
        views.DeleteComment.as_view(),
        name='delete_comment',
    ),
    # Posts in category overview page
    path(
        'category/<slug:category_slug>/',
        views.CategoryView.as_view(),
        name='category_posts',
    ),
]
