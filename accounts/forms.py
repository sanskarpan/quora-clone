from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    """
    Form for user registration extending Django's UserCreationForm
    with additional email field
    """
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def clean_email(self):
        """
        Validate that the email is unique
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user's username and email
    """
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']
        
    def clean_email(self):
        """
        Validate that the email is unique, excluding the current user
        """
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user's profile information
    """
    class Meta:
        model = Profile
        fields = ['bio']