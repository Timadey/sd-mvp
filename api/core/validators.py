import re

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _



@deconstructible
class PhoneNumberValidator(validators.RegexValidator):
    regex = r'^\+?1?\d{9,15}$'
    message = "Phone number must be entered in the format: +999999999"
    flags = 0

def password_validator(password):
    """Validate user password
    Criteria
        1. Minimum length of 8 characters.
        2. At least one lowercase letter.
        3. At least one uppercase letter.
        4. At least one digit.
        5. At least one special character.
    """

    if len(password) < 8:
        raise ValidationError(_("Password must be at least 8 characters long"))

    if not re.search(r'[a-z]', password):
        raise ValidationError(_("Password must contain at least one lowercase letter"))

    if not re.search(r'[A-Z]', password):
        raise ValidationError(_("Password must contain at least one uppercase letter"))

    if not re.search(r'[0-9]', password):
        raise ValidationError(_("Password must contain at least one digit"))

    if not re.search(r'[!@#$%^&*()-_=+{};:,<.>]', password):
        raise ValidationError(_("Password must contain at least one special character"))

    return password