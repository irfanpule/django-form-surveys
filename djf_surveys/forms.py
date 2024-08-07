from typing import List, Tuple

from django import forms
from django.db import transaction
from django.core.mail import send_mail, BadHeaderError
from django.core.validators import MaxLengthValidator, MinLengthValidator, MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from djf_surveys.models import Answer, TYPE_FIELD, UserAnswer, Question
from djf_surveys.widgets import CheckboxSelectMultipleSurvey, RadioSelectSurvey, DateSurvey, RatingSurvey
from djf_surveys.app_settings import DATE_INPUT_FORMAT, SURVEY_FIELD_VALIDATORS, SURVEY_EMAIL_FROM
from djf_surveys.validators import (
    RatingValidator, SurveyEmailValidator, TermsEmailValidator, TermsTextValidator, TermsTextAreaValidator,
    TermsNumberValidator
)


def make_choices(question: Question) -> List[Tuple[str, str]]:
    choices = []
    for choice in question.choices.split(','):
        choice = choice.strip()
        choices.append((choice.replace(' ', '_').lower(), choice))
    return choices


class BaseSurveyForm(forms.Form):

    def __init__(self, survey, user, *args, **kwargs):
        self.survey = survey
        self.user = user if user.is_authenticated else None
        self.field_names = []
        self.questions = self.survey.questions.all().order_by('ordering')
        super().__init__(*args, **kwargs)

        for question in self.questions:
            # to generate field name
            field_name = f'field_survey_{question.id}'

            if question.type_field == TYPE_FIELD.multi_select:
                choices = make_choices(question)
                self.fields[field_name] = forms.MultipleChoiceField(
                    choices=choices, label=question.label,
                    widget=CheckboxSelectMultipleSurvey,
                )
            elif question.type_field == TYPE_FIELD.radio:
                choices = make_choices(question)
                self.fields[field_name] = forms.ChoiceField(
                    choices=choices, label=question.label,
                    widget=RadioSelectSurvey
                )
            elif question.type_field == TYPE_FIELD.select:
                choices = make_choices(question)
                empty_choice = [("", _("Choose"))]
                choices = empty_choice + choices
                self.fields[field_name] = forms.ChoiceField(
                    choices=choices, label=question.label
                )
            elif question.type_field == TYPE_FIELD.number:
                # add other terms validator
                validators = []
                if hasattr(question, 'termsvalidators'):
                    terms = TermsNumberValidator.to_object(question.termsvalidators.terms)
                    validators.append(MinValueValidator(terms.min_value))
                    validators.append(MaxValueValidator(terms.max_value))
                else:
                    terms = TermsNumberValidator()
                    validators.append(MinValueValidator(terms.min_value))
                    validators.append(MaxValueValidator(terms.max_value))

                self.fields[field_name] = forms.IntegerField(label=question.label, validators=validators)
            elif question.type_field == TYPE_FIELD.url:
                self.fields[field_name] = forms.URLField(
                    label=question.label,
                    validators=[MaxLengthValidator(SURVEY_FIELD_VALIDATORS['max_length']['url'])]
                )
            elif question.type_field == TYPE_FIELD.email:
                validators = [MaxLengthValidator(SURVEY_FIELD_VALIDATORS['max_length']['email'])]

                # add other terms validator
                if hasattr(question, 'termsvalidators'):
                    terms = TermsEmailValidator.to_object(question.termsvalidators.terms)
                    validators.append(SurveyEmailValidator(terms))

                self.fields[field_name] = forms.EmailField(label=question.label, validators=validators)

            elif question.type_field == TYPE_FIELD.date:
                self.fields[field_name] = forms.DateField(
                    label=question.label, widget=DateSurvey(),
                    input_formats=DATE_INPUT_FORMAT
                )
            elif question.type_field == TYPE_FIELD.text_area:
                # add other terms validator
                validators = []
                if hasattr(question, 'termsvalidators'):
                    terms = TermsTextAreaValidator.to_object(question.termsvalidators.terms)
                    validators.append(MinLengthValidator(terms.min_length))
                    validators.append(MaxLengthValidator(terms.max_length))
                else:
                    terms = TermsTextAreaValidator()
                    validators.append(MinLengthValidator(terms.min_length))
                    validators.append(MaxLengthValidator(terms.max_length))

                self.fields[field_name] = forms.CharField(
                    label=question.label, widget=forms.Textarea, validators=validators)

            elif question.type_field == TYPE_FIELD.rating:
                if not question.choices:  # use 5 as default for backward compatibility
                    question.choices = 5
                self.fields[field_name] = forms.CharField(
                    label=question.label, widget=RatingSurvey,
                    validators=[MaxLengthValidator(len(str(int(question.choices)))),
                                RatingValidator(int(question.choices))]
                )
                self.fields[field_name].widget.num_ratings = int(question.choices)
            else:
                # add other terms validator
                validators = []
                if hasattr(question, 'termsvalidators'):
                    terms = TermsTextValidator.to_object(question.termsvalidators.terms)
                    validators.append(MinLengthValidator(terms.min_length))
                    validators.append(MaxLengthValidator(terms.max_length))
                else:
                    terms = TermsTextValidator()
                    validators.append(MinLengthValidator(terms.min_length))
                    validators.append(MaxLengthValidator(terms.max_length))

                self.fields[field_name] = forms.CharField(
                    label=question.label, validators=validators)

            self.fields[field_name].required = question.required
            self.fields[field_name].help_text = question.help_text
            self.field_names.append(field_name)

    def clean(self):
        cleaned_data = super().clean()

        for field_name in self.field_names:
            try:
                field = cleaned_data[field_name]
            except KeyError:
                raise forms.ValidationError("You must enter valid data")

            if self.fields[field_name].required and not field:
                self.add_error(field_name, 'This field is required')

        return cleaned_data


class CreateSurveyForm(BaseSurveyForm):

    @transaction.atomic
    def save(self):
        cleaned_data = super().clean()

        user_answer = UserAnswer.objects.create(
            survey=self.survey, user=self.user
        )
        for question in self.questions:
            field_name = f'field_survey_{question.id}'

            if question.type_field == TYPE_FIELD.multi_select:
                value = ",".join(cleaned_data[field_name])
            else:
                value = cleaned_data[field_name]

            Answer.objects.create(
                question=question, value=value, user_answer=user_answer
            )

        if self.survey.notification_to and SURVEY_EMAIL_FROM:
            try:
                user_answer_count = UserAnswer.objects.filter(survey=self.survey).count()
                send_mail(
                    _('Notification {survey_name}').format(survey_name=self.survey.name),
                    _('You have received one new response. '
                      'The total number of responses is currently {count}').format(count=user_answer_count),
                    SURVEY_EMAIL_FROM,
                    self.survey.notification_to.split(","),
                    fail_silently=False,
                )
            except (BadHeaderError, ConnectionError) as e:
                print(e)


class EditSurveyForm(BaseSurveyForm):

    def __init__(self, user_answer, *args, **kwargs):
        self.survey = user_answer.survey
        self.user_answer = user_answer
        super().__init__(survey=self.survey, user=user_answer.user, *args, **kwargs)
        self._set_initial_data()

    def _set_initial_data(self):
        answers = self.user_answer.answer_set.all()

        for answer in answers:
            field_name = f'field_survey_{answer.question.id}'
            if answer.question.type_field == TYPE_FIELD.multi_select:
                self.fields[field_name].initial = answer.value.split(',')
            else:
                self.fields[field_name].initial = answer.value

    @transaction.atomic
    def save(self):
        cleaned_data = super().clean()
        self.user_answer.survey = self.survey
        self.user_answer.user = self.user
        self.user_answer.save()

        for question in self.questions:
            field_name = f'field_survey_{question.id}'

            if question.type_field == TYPE_FIELD.multi_select:
                value = ",".join(cleaned_data[field_name])
            else:
                value = cleaned_data[field_name]

            answer, created = Answer.objects.get_or_create(
                question=question, user_answer=self.user_answer,
                defaults={'question_id': question.id, 'user_answer_id': self.user_answer.id}
            )

            if not created and answer:
                answer.value = value
                answer.save()
