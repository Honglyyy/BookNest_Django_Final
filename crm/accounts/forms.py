from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    # email = forms.EmailField(
    #     required=True,
    #     widget=forms.EmailInput(attrs={
    #         'class': 'form-input',
    #         'placeholder': 'Enter your email'
    #     })
    # )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        # Customize username field
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Choose a username'
        })
        self.fields['username'].label = 'Username'
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'

        # Customize password1 field
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Enter password'
        })
        self.fields['password1'].label = 'Password'
        self.fields[
            'password1'].help_text = 'Your password must contain at least 8 characters and cannot be entirely numeric.'

        # Customize password2 field
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirm password'
        })
        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].help_text = 'Enter the same password as before, for verification.'


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Enter your username'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Enter your password'
        })