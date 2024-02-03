from django.test import TestCase
from django.core.exceptions import ValidationError
from djf_surveys.validators import RatingValidator


class ValidationForm(TestCase):
    def test_validate_rating(self):
        with self.assertRaises(ValidationError):
            val = RatingValidator(10)
            val(0)

        with self.assertRaises(ValidationError):
            val = RatingValidator(10)
            val(100)

        val = RatingValidator(5)
        val(2)
