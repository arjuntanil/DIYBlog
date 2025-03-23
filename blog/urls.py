from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog-list'),
    path('post/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('post/create/', views.create_blog_post, name='blog-create'),
    path('post/<int:pk>/update/', views.update_blog_post, name='blog-update'),
    path('post/<int:pk>/delete/', views.delete_blog_post, name='blog-delete'),
    path('post/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('post/<int:pk>/like/', views.toggle_like, name='toggle-like'),
    path('post/<int:pk>/check-password/', views.check_post_password, name='check-post-password'),
    path('bloggers/', views.BloggerListView.as_view(), name='blogger-list'),
    path('blogger/<int:pk>/', views.BloggerDetailView.as_view(), name='blogger-detail'),
    path('register/', views.register, name='register'),
]
