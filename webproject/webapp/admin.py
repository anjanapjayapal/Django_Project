from django.contrib import admin
from django.contrib.auth.models import User
from .models import BlogPost, Profile, SharedImage, Comment

# 🔹 Register Profile model for user management
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_number')
    search_fields = ('user__username', 'contact_number')

admin.site.register(Profile, ProfileAdmin)

# 🔹 Register BlogPost model for post management
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username')
    list_filter = ('created_at',)

admin.site.register(BlogPost, BlogPostAdmin)

# 🔹 Register SharedImage model
class SharedImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('user__username',)

admin.site.register(SharedImage, SharedImageAdmin)

# 🔹 Register Comment model
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('post__title', 'author__username')

admin.site.register(Comment, CommentAdmin)
