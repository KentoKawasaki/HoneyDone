from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.db import models

from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    
    username = None
    first_name = None
    last_name = None

    user_name_validator = UnicodeUsernameValidator()
    user_name = models.CharField(
        _('your name'),
        max_length=150,
        help_text=_(
            'Required. 150 characters or fewer.'
            ' Letters, digits and @/./+/-/_ only.'),
        validators=[user_name_validator],
    )
    
    email = models.EmailField(
        _('email adress'),
        unique=True,
        error_messages={
            'unique': _("A user with that email adress already exists.")
        },
    )

    objects = CustomUserManager()
    
    # EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    
    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.email
