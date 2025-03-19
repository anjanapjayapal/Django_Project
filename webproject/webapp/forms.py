from django import forms
from django.contrib.auth.models import User
from .models import Profile, BlogPost, SharedImage, Comment


from django import forms
from django.contrib.auth.models import User
from .models import Profile
import re  # ✅ Import regex for validation


import re
from django import forms
from django.contrib.auth.models import User
from webapp.models import Profile  # Import your Profile model

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm Password"
    )
    contact_number = forms.CharField(
        max_length=15,
        required=True,
        help_text="Enter a valid phone number (digits only).",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    profile_pic = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


# 🔹 User Profile Update Form
from django import forms
from django.contrib.auth.models import User
from .models import Profile
import re  # ✅ Import regex for validation

class UserProfileUpdateForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False)
    contact_number = forms.CharField(
        max_length=15,
        required=False,
        help_text="Enter a valid phone number (digits only)."
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'profile'):
            self.fields['profile_pic'].initial = self.instance.profile.profile_pic
            self.fields['contact_number'].initial = self.instance.profile.contact_number

    # ✅ Validate First Name & Last Name (Only letters)
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match("^[A-Za-z]*$", first_name):
            raise forms.ValidationError("First name should contain only letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match("^[A-Za-z]*$", last_name):
            raise forms.ValidationError("Last name should contain only letters.")
        return last_name

    # ✅ Validate Email Format
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(username=self.instance.username).exists():
            raise forms.ValidationError("This email is already in use. Please use a different one.")
        return email

    # ✅ Validate Contact Number (Only digits, 10-15 characters)
    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if contact_number and not re.match("^[0-9]{10}$", contact_number):
            raise forms.ValidationError("Enter a valid phone number.")
        return contact_number

    # ✅ Save Profile Data Along with User Data
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)

            profile_pic = self.cleaned_data.get('profile_pic')
            if profile_pic:
                profile.profile_pic = profile_pic

            profile.contact_number = self.cleaned_data.get('contact_number')
            profile.save()
        return user



# 🔹 Blog Post Form
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']


# 🔹 Image Upload Form
class SharedImageForm(forms.ModelForm):
    class Meta:
        model = SharedImage
        fields = ['image', 'caption']


# 🔹 Comment Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
