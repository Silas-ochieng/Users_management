# auth_project/accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('normal', 'Normal User'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='normal')

    # New fields for profile picture, bio, and about
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True, help_text="A short biography visible on your profile.")
    about = models.TextField(blank=True, null=True, help_text="Tell us more about yourself, your interests, etc.")

    # Add related_name to avoid clashes with auth.User if it were also used
    # This is a common requirement when defining a custom user model
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions '
                  'granted to each of their groups.',
        related_name="custom_user_groups", # Changed from default 'auth.User.groups'
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_permissions", # Changed from default 'auth.User.user_permissions'
        related_query_name="custom_user",
    )


    def __str__(self):
        return self.username