from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_rating(value):
    try:
        rating = int(value)
    except (TypeError, ValueError):
        raise ValidationError(
            _('%(value)s is not a number.'),
            params={'value': value},
        )

    if rating > 5:
        raise ValidationError(
            _('Value cannot be greater than 5.')
        )

    if rating < 1:
        raise ValidationError(
            _('Value cannot be less than 1.')
        )

