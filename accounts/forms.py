# auth_project/accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'user_type') # Keep this for basic registration

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_picture', 'bio', 'about')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            # For profile_picture, the default ClearableFileInput is usually fine.
            # If you want to add a Bootstrap class to it, you'd use:
            # 'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            # Note: Directly adding 'form-control' to a file input via widget_tweaks
            # makes it look a bit odd, Bootstrap suggests custom file inputs
            # or letting the default browser one show.
            # However, widget_tweaks can still apply it if you want.
        }

    # Custom __init__ to manage user_type field access for non-admins
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure 'user_type' is in fields before trying to access it
        if 'user_type' in self.fields:
            # If the instance exists (i.e., we are editing an existing user)
            # AND the user is NOT staff/superuser
            if self.instance and not self.instance.is_staff and not self.instance.is_superuser:
                self.fields['user_type'].widget.attrs['disabled'] = 'disabled'
                self.fields['user_type'].help_text = "Only administrators can change user type."


class AdminUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name',
                  'profile_picture', 'bio', 'about',
                  'is_active', 'is_staff', 'is_superuser', 'user_type')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            # 'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }