from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class TermsEmailValidator(object):
    type_filter = ""
    email_domain = ""

    def __init__(self, type_filter: str, email_domain: str):
        self.type_filter = type_filter
        self.email_domain = email_domain

    def to_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def to_object(cls, data: dict):
        cls.type_filter = data.get("type_filter")
        cls.email_domain = data.get("email_domain")
        return cls


class RatingValidator(object):
    def __init__(self, max):
        self.max = max

    def __call__(self, value):
        try:
            rating = int(value)
        except (TypeError, ValueError):
            raise ValidationError(
                _('%ss is not a number.' % value)
            )

        if rating > self.max:
            raise ValidationError(
                _('Value cannot be greater than maximum allowed number of ratings.')
            )

        if rating < 1:
            raise ValidationError(
                _('Value cannot be less than 1.')
            )

class SurveyEmailValidator:

    def __init__(self, terms: TermsEmailValidator):
        self.terms = terms

    def __call__(self, value):
        try:
            domain = value.split('@')[1]
        except IndexError:
            raise ValidationError(_('Invalid email'))

        if self.terms.type_filter and self.terms.email_domain:
            if self.terms.type_filter == 'whitelist' and domain not in self.terms.email_domain:
                raise ValidationError(
                    _(f'Your email is not allowed. Allowed email domains are {self.terms.email_domain}'))
            elif self.terms.type_filter == 'blacklist' and domain in self.terms.email_domain:
                raise ValidationError(
                    _(f'Your email is not allowed. Email domains that are not allowed are {self.terms.email_domain}'))
