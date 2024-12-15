from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

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