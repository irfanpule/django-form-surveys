from django import forms
from surveys.models import Survey, Answer, TYPE_FIELD
from surveys.utils import make_choices


class SurveyForm(forms.Form):

    def __init__(self, survey, *args, **kwargs):
        self.survey = survey
        self.field_names = []
        self.questions = self.survey.questions.all()
        super().__init__(*args, **kwargs)

        for question in self.questions:
            # to generate field name
            field_name = f'field_survey_{question.id}'

            if question.type_field == TYPE_FIELD.multi_select:
                self.fields[field_name] = forms.MultipleChoiceField(
                    choices=make_choices(question), label=question.label,
                )
            elif question.type_field == TYPE_FIELD.radio:
                self.fields[field_name] = forms.ChoiceField(
                    choices=make_choices(question), label=question.label,
                    widget=forms.RadioSelect
                )
            elif question.type_field == TYPE_FIELD.select:
                self.fields[field_name] = forms.ChoiceField(
                    choices=make_choices(question), label=question.label
                )
            elif question.type_field == TYPE_FIELD.number:
                self.fields[field_name] = forms.IntegerField(label=question.label)
            elif question.type_field == TYPE_FIELD.text_area:
                self.fields[field_name] = forms.CharField(
                    label=question.label, widget=forms.Textarea
                )
            else:
                self.fields[field_name] = forms.CharField(label=question.label)

            self.fields[field_name].required = question.required
            self.fields[field_name].help_text = question.help_text
            self.field_names.append(field_name)

            # to set initial data
            if hasattr(question, 'answer'):
                if question.type_field == TYPE_FIELD.multi_select:
                    self.fields[field_name].initial = question.answer.value.split(',')
                else:
                    self.fields[field_name].initial = question.answer.value

    def clean(self):
        cleaned_data = super().clean()

        for field_name in self.field_names:
            if self.fields[field_name].required and not cleaned_data[field_name]:
                self.add_error(field_name, 'This field is required')

        return cleaned_data

    def save(self):
        cleaned_data = super().clean()

        for question in self.questions:
            field_name = f'field_survey_{question.id}'

            if question.type_field == TYPE_FIELD.multi_select:
                value = ",".join(cleaned_data[field_name])
            else:
                value = cleaned_data[field_name]

            answer, created = Answer.objects.get_or_create(
                question=question, defaults={'value': value}
            )

            if answer:
                answer.value = value
                answer.save()
