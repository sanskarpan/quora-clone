
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.decorators.http import require_http_methods
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

class CustomLoginView(LoginView):
    """
    Custom login view with enhanced template
    """
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


# Replace the class-based logout view with a function-based view
@login_required
@require_http_methods(["GET"])
def logout_view(request):
    """
    Custom logout view that properly logs out the user and redirects to home
    """
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')


def register(request):
    """
    User registration view
    """
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    """
    User profile view for viewing and updating user information
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'accounts/profile.html', context)