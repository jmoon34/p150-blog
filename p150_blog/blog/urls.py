from django.urls import path, include
from . import views
from .views import (
    PostListView,
    PostView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    SearchPostListView,
    CommentDeleteView,
    CommentUpdateView,
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
)


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('category/', views.category, name='blog-category'),
    path('category/<str:title>/', CategoryListView.as_view(),
         name='category-posts'),
    path('category/new', CategoryCreateView.as_view(), name='category-create'),
    path('category/<str:title>/update', CategoryUpdateView.as_view(),
         name='category-update'),
    path('category/<str:title>/delete', CategoryDeleteView.as_view(),
         name='category-delete'),
    path('post/<int:pk>/', PostView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(),
         name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(),
         name='post-delete'),
    path('post/<int:pk_post>/comment/<int:pk_comment>/delete', CommentDeleteView.as_view(),
         name='comment-delete'),
    path('post/<int:pk_post>/comment/<int:pk_comment>/update',
         CommentUpdateView.as_view(), name='comment-update'),
    path('user/<str:username>/', UserPostListView.as_view(),
         name='user-posts'),
    path('search/', SearchPostListView.as_view(), name='search-list-view'),
]

