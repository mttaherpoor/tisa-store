from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

import re


class PasswordCharValidator:
    """
    Validate that the password only contains allowed characters.
    """
    def __init__(self, min_length=None):
        self.min_length = min_length

    def validate(self, password, user=None):
        if not re.match(r'^[A-Za-z0-9@#$&_\-\.!]+$', password):
            raise ValidationError(
                _("رمز عبور فقط می‌تواند شامل حروف انگلیسی، اعداد و علامت‌های @ # $ & _ - ! باشد."),
                code='invalid_password',
            )

    def get_help_text(self):
        return _("رمز عبور فقط می‌تواند شامل حروف انگلیسی، اعداد و علامت‌های @ # $ & _ - ! باشد.")


def validator(message_param):
    """Check if value only contains allowed characters."""
    return RegexValidator(
        regex=r'^[A-Za-z0-9@#$&_\-\.!]+$',
        message=f'{message_param} فقط می‌تواند شامل حروف انگلیسی، اعداد و علامت‌های @ # $ & _ - ! باشد.'
        )

username_validator = validator('نام کاربری')
email_validator = validator('ایمیل')