from django.urls import path, include
from django.views.generic.dates import ArchiveIndexView
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
    PostArchiveIndexView,
    PostYearArchiveView,
    PostMonthArchiveView,
)
from .models import Post

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('archive/', PostArchiveIndexView.as_view(), name='archive-index'),
    path('archive/<int:year>/', PostYearArchiveView.as_view(), name='archive-year'),
    path('archive/<int:year>/<int:month>',
         PostMonthArchiveView.as_view(month_format='%m'), name='archive-month'),
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

