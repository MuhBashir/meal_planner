from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserProfileForm(UserChangeForm):
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Remove specific password validation error messages

        self.fields['password'].widget = forms.HiddenInput()
        # Hide the rest of the default password validation messages
        self.fields["username"].help_text = ""
    
    class Meta:
        model = User
        fields = ['username',  'email']


class UserRegistrationForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Remove specific password validation error messages
        self.fields['password2'].error_messages = {
            'password_mismatch': 'Your passwords do not match.'
        }
        
        # Hide the rest of the default password validation messages
        self.fields['password2'].help_text = ''
        self.fields["password1"].help_text = ''
        self.fields["username"].help_text = ""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    