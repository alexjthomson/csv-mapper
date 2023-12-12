from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class ComplexPasswordValidator:
    """
    Validates that a password is complex by checking it contains:
    - At least one uppercase letter.
    - At least one lowercase letter.
    - At least one number.
    - At least one symbol.
    """

    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(_('Password must contain at least one uppercase letter.'), code='password_no_upper')

        if not re.findall('[a-z]', password):
            raise ValidationError(_('Password must contain at least one lowercase letter.'), code='password_no_lower')

        if not re.findall('[0-9]', password):
            raise ValidationError(_('Password must contain at least one digit.'), code='password_no_digit')

        if not re.findall('[^A-Za-z0-9]', password):
            raise ValidationError(_('Password must contain at least one symbol.'), code='password_no_symbol')

    def get_help_text(self):
        return _(
            "Your password must contain at least one uppercase letter, one lowercase letter, "
            "one number, and one symbol."
        )

class NoSpacePasswordValidator:
    """
    Validates that a password does not contains a space.
    """

    def validate(self, password, user=None):
        if ' ' in password:
            raise ValidationError(_('Password cannot contain spaces.'), code='password_invalid_character')

    def get_help_text(self):
        return _(
            "Your password can't contain a space."
        )

class ValidCharsetPasswordValidator:
    """
    Validates that a password only contains valid characters.
    """

    def __init__(self, allowed_charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_+=}{][|:;'\"><,.?/\\"):
        self.allowed_charset = allowed_charset

    def validate(self, password, user=None):
        if not all(char in self.allowed_charset for char in password):
            raise ValidationError(_('Password must contain valid characters.'), code='password_invalid_character')

    def get_help_text(self):
        return _(
            "Your password must only contain valid ASCII characters."
        )