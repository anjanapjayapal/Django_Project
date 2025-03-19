from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import ProfileUpdateView, admin_dashboard, delete_user, block_user, delete_post
from django.urls import reverse_lazy



app_name = 'webapp'

urlpatterns = [
    path('', views.homePage, name='home'),
    path('profile/', views.view_profile, name='view_profile'),
    path('register/', views.registerUser, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logOut, name='logout'),
    path('profile/update/', ProfileUpdateView.as_view(), name='update_profile'),


    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html',
         success_url=reverse_lazy('webapp:password_reset_done')), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),


    path('blogs/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('blogs/', views.blog_list, name='blog_list'),  # View all blogs
    path('blogs/new/', views.create_blog, name='create_blog'),  # Create new blog
    path('blogs/edit/<int:post_id>/', views.edit_blog, name='edit_blog'),  # Edit blog
    path('blogs/delete/<int:post_id>/', views.delete_blog, name='delete_blog'),  # Delete blog

    # 🔹 Image Sharing URLs
    path('gallery/', views.image_gallery, name='image_gallery'),
    path('gallery/upload/', views.upload_image, name='upload_image'),


    # 🔹 Comment URLs

    path('comments/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comments/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),


    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('admin/block-user/<int:user_id>/', block_user, name='block_user'),
    path('admin/delete-post/<int:post_id>/', delete_post, name='delete_post'),

]
