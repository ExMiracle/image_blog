from django.urls import path
from .views import (PostListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView,
                    PostListAPIView,
                    UserPostListAPIView,
                    )
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name = 'blog-home'),
    path('api/', PostListAPIView.as_view()),
    path('api/user/<str:username>/posts/', UserPostListAPIView.as_view()),
    path('user/<str:username>/posts/', UserPostListView.as_view(), name = 'profile-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name = 'post-delete'),
    path('about/', views.about, name = 'blog-about')
]
