from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .validators import username_validator,email_validator

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150,unique=True,validators=[username_validator])
    email = models.EmailField(unique=True,validators=[email_validator])
    profile_image = models.ImageField(_("Profile Image"),upload_to="accounts/profile_image/",blank=True)