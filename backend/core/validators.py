from django.core.validators import RegexValidator
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
                _("Password can only contain English letters, numbers, and the following symbols: @ # $ & _ - !"),
                code='invalid_password',
            )

    def get_help_text(self):
        return _("Password can only contain English letters, numbers, and the following symbols: @ # $ & _ - !")


def validator(message_param):
    """
    Check if value only contains allowed characters.
    """
    return RegexValidator(
        regex=r'^[A-Za-z0-9@#$&_\-\.!]+$',
        message=f'{message_param} can only contain English letters, numbers, and the following symbols: @ # $ & _ - !'
    )


username_validator = validator('Username')
email_validator = validator('Email')


def validate_file_size(file):
    max_size_mb = 5
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(
            f"File size must not exceed {max_size_mb} MB."
        )
    