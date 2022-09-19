from typing import List, Tuple

from django import forms
from django.db import transaction
from django.core.validators import MaxLengthValidator

from djf_surveys.models import Answer, TYPE_FIELD, UserAnswer, Question
from djf_surveys.widgets import CheckboxSelectMultipleSurvey, RadioSelectSurvey, DateSurvey, RatingSurvey
from djf_surveys.app_settings import DATE_INPUT_FORMAT, SURVEY_FIELD_VALIDATORS
from djf_surveys.validators import validate_rating


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
                self.fields[field_name] = forms.ChoiceField(
                    choices=choices, label=question.label
                )
            elif question.type_field == TYPE_FIELD.number:
                self.fields[field_name] = forms.IntegerField(label=question.label)
            elif question.type_field == TYPE_FIELD.url:
                self.fields[field_name] = forms.URLField(
                    label=question.label,
                    validators=[MaxLengthValidator(SURVEY_FIELD_VALIDATORS['max_length']['url'])]
                )
            elif question.type_field == TYPE_FIELD.email:
                self.fields[field_name] = forms.EmailField(
                    label=question.label,
                    validators=[MaxLengthValidator(SURVEY_FIELD_VALIDATORS['max_length']['email'])]
                )
            elif question.type_field == TYPE_FIELD.date:
                self.fields[field_name] = forms.DateField(
                    label=question.label, widget=DateSurvey(),
                    input_formats=DATE_INPUT_FORMAT
                )
            elif question.type_field == TYPE_FIELD.text_area:
                self.fields[field_name] = forms.CharField(
                    label=question.label, widget=forms.Textarea
                )
            elif question.type_field == TYPE_FIELD.rating:
                self.fields[field_name] = forms.CharField(
                    label=question.label, widget=RatingSurvey,
                    validators=[MaxLengthValidator(1), validate_rating]
                )
            else:
                self.fields[field_name] = forms.CharField(
                    label=question.label,
                    validators=[MaxLengthValidator(SURVEY_FIELD_VALIDATORS['max_length']['text'])]
                )

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
