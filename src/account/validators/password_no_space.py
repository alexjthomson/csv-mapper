from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

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