from django.core.exceptions import ValidationError
from django.test import TestCase
from account.validators import ComplexPasswordValidator, NoSpacePasswordValidator, ValidCharsetPasswordValidator

class TestPasswordValidators(TestCase):
    def test_complex_password_validator_success(self):
        validator = ComplexPasswordValidator()
        try:
            # Valid password with all required components
            validator.validate('Password1!')
        except ValidationError:
            self.fail("ComplexPasswordValidator raised ValidationError unexpectedly!")

    def test_complex_password_validator_no_uppercase(self):
        validator = ComplexPasswordValidator()
        with self.assertRaisesMessage(ValidationError, 'Password must contain at least one uppercase letter.'):
            validator.validate('password1!')

    def test_complex_password_validator_no_lowercase(self):
        validator = ComplexPasswordValidator()
        with self.assertRaisesMessage(ValidationError, 'Password must contain at least one lowercase letter.'):
            validator.validate('PASSWORD1!')

    def test_complex_password_validator_no_digit(self):
        validator = ComplexPasswordValidator()
        with self.assertRaisesMessage(ValidationError, 'Password must contain at least one digit.'):
            validator.validate('Password!')

    def test_complex_password_validator_no_symbol(self):
        validator = ComplexPasswordValidator()
        with self.assertRaisesMessage(ValidationError, 'Password must contain at least one symbol.'):
            validator.validate('Password1')

    def test_no_space_password_validator_success(self):
        validator = NoSpacePasswordValidator()
        try:
            # Valid password without spaces
            validator.validate('Password1!')
        except ValidationError:
            self.fail("NoSpacePasswordValidator raised ValidationError unexpectedly!")

    def test_no_space_password_validator_with_space(self):
        validator = NoSpacePasswordValidator()
        with self.assertRaisesMessage(ValidationError, 'Password cannot contain spaces.'):
            validator.validate('Password 1!')

    def test_valid_charset_password_validator_success(self):
        validator = ValidCharsetPasswordValidator()
        try:
            # Valid password with allowed characters
            validator.validate('Password1!')
        except ValidationError:
            self.fail("ValidCharsetPasswordValidator raised ValidationError unexpectedly!")

    def test_valid_charset_password_validator_invalid_character(self):
        validator = ValidCharsetPasswordValidator()
        with self.assertRaisesMessage(ValidationError, 'Password must contain valid characters.'):
            validator.validate('Password1!🚀')
