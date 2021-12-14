from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.core.exceptions import ValidationError

from .models import CustomUser

from django.utils.translation import gettext, gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    """
        Form for creating new users
    """

    # email = forms.EmailField(
    #     max_length=60,
    #     label='Email',
    #     help_text='Required. Add a valid email address')
    # password1 = forms.CharField(widget=forms.PasswordInput(
    #     attrs={'class': 'form-control'}),
    #     label="Password")
    # password2 = forms.CharField(widget=forms.PasswordInput(
    #     attrs={'class': 'form-control'}),
    #     label="Password (again)")
    
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')
        field_order = ('email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        email_objects = CustomUser.objects.filter(email=email).exists()
        if email_objects:
            raise forms.ValidationError(
                'このメールアドレスは既に登録されています。'
            )

        return email


class CustomUserAuthenticationForm(forms.Form):
    """
        Form for Logging in users
    """
    email = forms.EmailField(
        max_length=60,
        widget=forms.EmailInput(attrs={'autofocus': True}),
        label='ID(Email)',
        help_text='Required. Please add your Email.')
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(email)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)
    
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        username_field = CustomUser._meta.get_field(CustomUser.USERNAME_FIELD)
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'email': username_field.verbose_name},
        )

class CustomUserChangeForm(UserChangeForm):
    """
        Changing User info
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'user_name')
        
        # widgets = {
        #     'email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     'user_name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        # }

    # def __init__(self, *args, **kwargs):
    #     """
    #         specifying styles to fields
    #     """
    #     super(CustomUserChangeForm, self).__init__(*args, **kwargs)
    #     for field in (self.fields['email'], self.fields['user_name']):
    #         field.widget.attrs.update({'class': 'form-control'})