from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Profile, BlogPost, SharedImage, Comment
from .forms import UserProfileUpdateForm, BlogPostForm, SharedImageForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from django.db.models.signals import post_save
from django.dispatch import receiver




from django.contrib.auth.decorators import user_passes_test

from .forms import UserRegistrationForm

def registerUser(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect('webapp:login')

    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


from django.contrib.auth.models import User
from webapp.models import Profile

from django.http import HttpResponse
from .forms import UserRegistrationForm





class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User  # ✅ Use User model to update username, name, email
    form_class = UserProfileUpdateForm  # ✅ Use updated form
    template_name = 'update_profile.html'
    success_url = reverse_lazy('webapp:view_profile')

    def get_object(self, queryset=None):
        return self.request.user



""" def loginUser(request):  # Renamed function
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('webapp:home')
        else:
            messages.info(request, "Invalid username or password.")

    return render(request, 'login.html')"""


def logOut(request):
    logout(request)
    return redirect('webapp:home')


def homePage(request):

    return render(request, 'home.html')



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)  # Auto-create profile if it doesn't exist


@login_required
def view_profile(request):
    user = request.user
    blogs = BlogPost.objects.filter(author=user)  # Fetch blogs by the user
    images = SharedImage.objects.filter(user=user)  # Fetch images by the user

    context = {
        'user': user,
        'blogs': blogs,
        'images': images
    }
    return render(request, 'profile.html', context)



# 🔹 View All Blog Posts (Only for Logged-in Users)
@login_required
def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')  # Show newest first
    return render(request, 'blog_list.html', {'posts': posts})

# 🔹 Create a New Blog Post
@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user  # Assign the logged-in user
            blog.save()
            return redirect('webapp:blog_list')  # Redirect to blog list after posting
    else:
        form = BlogPostForm()

    return render(request, 'blog_form.html', {'form': form})

# 🔹 Edit Blog Post (Only Author Can Edit)
@login_required
def edit_blog(request, post_id):
    blog = get_object_or_404(BlogPost, id=post_id, author=request.user)  # Only allow the author to edit
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('webapp:blog_list')

    else:
        form = BlogPostForm(instance=blog)

    return render(request, 'blog_form.html', {'form': form})

# 🔹 Delete Blog Post (Only Author Can Delete)
@login_required
def delete_blog(request, post_id):
    blog = get_object_or_404(BlogPost, id=post_id, author=request.user)  # Ensure only author can delete
    if request.method == 'POST':
        blog.delete()
        return redirect('webapp:blog_list')

    return render(request, 'blog_confirm_delete.html', {'blog': blog})


# 🔹 View All Shared Images
@login_required
def image_gallery(request):
    images = SharedImage.objects.all().order_by('-uploaded_at')
    return render(request, 'image_gallery.html', {'images': images})

# 🔹 Upload an Image
@login_required
def upload_image(request):
    if request.method == 'POST':
        form = SharedImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            return redirect('webapp:image_gallery')
    else:
        form = SharedImageForm()

    return render(request, 'upload_image.html', {'form': form})


def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = post.comments.all().order_by('-created_at')  # Fetch comments for this post

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # Assign the logged-in user as the comment author
            comment.save()
            return redirect('webapp:blog_detail', post_id=post.id)  # Refresh page after adding comment
    else:
        form = CommentForm()

    return render(request, 'blog_detail.html', {'post': post, 'comments': comments, 'form': form})


# 🔹 Edit Comment (Only Author Can Edit)
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)  # Ensure only the author can edit

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('webapp:blog_detail', post_id=comment.post.id)

    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form})

# 🔹 Delete Comment (Only Author Can Delete)
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)  # Ensure only author can delete

    if request.method == 'POST':
        post_id = comment.post.id
        comment.delete()
        return redirect('webapp:blog_detail', post_id=post_id)

    return render(request, 'delete_comment.html', {'comment': comment})


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def blog_list(request):
    query = request.GET.get('q')  # Get search query
    posts = BlogPost.objects.all().order_by('-created_at')

    # 🔹 Apply Search Filter
    if query:
        posts = posts.filter(title__icontains=query)  # Search by title

    # 🔹 Add Pagination (5 posts per page)
    paginator = Paginator(posts, 5)  # Show 5 blogs per page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)  # Show first page if page number is not an integer
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # Show last page if out of range

    return render(request, 'blog_list.html', {'posts': posts, 'query': query})




# 🔹 Restrict admin panel to only superusers
def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.all()
    posts = BlogPost.objects.all()
    images = SharedImage.objects.all()  # ✅ Include images for dashboard stats
    return render(request, 'admin_dashboard.html', {'users': users, 'posts': posts, 'images': images})


@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('webapp:admin_dashboard')

@user_passes_test(is_admin)
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    return redirect('webapp:admin_dashboard')

@user_passes_test(is_admin)
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    post.delete()
    return redirect('webapp:admin_dashboard')


def save(self, commit=True):
    user = super().save(commit=False)
    if commit:
        user.save()
        profile, created = Profile.objects.get_or_create(user=user)

        profile_pic = self.cleaned_data.get('profile_pic')
        if profile_pic:  # ✅ Only update if a new image is uploaded
            profile.profile_pic = profile_pic

        profile.contact_number = self.cleaned_data.get('contact_number')
        profile.save()
    return user
