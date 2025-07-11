# auth_project/accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages # <--- ADDED: Import messages framework
from .forms import CustomUserCreationForm, CustomUserChangeForm, AdminUserChangeForm
from .models import CustomUser
from .tokens import account_activation_token

# Helper function to check if a user is an admin
def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'

def home_view(request):
    """
    Renders the homepage. Displays different content based on user authentication status.
    """
    return render(request, 'home.html')

# --- User Registration ---
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until email verification
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.' # Adjusted subject
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Registration successful! Please check your email to activate your account.')
            return render(request, 'accounts/registration_pending.html')
        else:
            # Add error messages from the form to the messages framework
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').capitalize()}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# --- User Verification ---
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated successfully! You are now logged in.')
        return redirect('profile') # Redirect to profile after activation
    else:
        messages.error(request, 'The activation link is invalid or has expired.')
        return render(request, 'accounts/activation_invalid.html')

# --- Profile Management ---
@login_required
def profile_view(request):
    # The template already accesses request.user directly, so no need to pass 'user' explicitly
    return render(request, 'accounts/profile.html')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        # <--- IMPORTANT: Pass request.FILES to the form for file uploads --->
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            # Handle user_type if it was disabled for non-admins in the form
            # Ensure the user_type isn't accidentally changed if the field was disabled in the form
            if not request.user.is_staff and not request.user.is_superuser:
                # Retrieve the original user_type from the database instance
                original_user_type = CustomUser.objects.get(pk=request.user.pk).user_type
                user.user_type = original_user_type # Restore the original user_type
            user.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error(s) below.')
            # Add specific form errors to messages for better user feedback
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').capitalize()}: {error}")
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important! To keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error(s) below.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').capitalize()}: {error}")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

# --- Admin Panel ---
@user_passes_test(is_admin)
def admin_user_list(request):
    users = CustomUser.objects.all().order_by('username') # Added ordering
    return render(request, 'accounts/admin_user_list.html', {'users': users})

@user_passes_test(is_admin)
def admin_user_edit(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        # <--- IMPORTANT: Pass request.FILES to the form for file uploads --->
        form = AdminUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} was successfully updated!')
            return redirect('admin_user_list')
        else:
            messages.error(request, 'Please correct the error(s) below.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').capitalize()}: {error}")
    else:
        form = AdminUserChangeForm(instance=user)
    return render(request, 'accounts/admin_user_edit.html', {'form': form, 'user': user})