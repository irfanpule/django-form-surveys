from django import forms


class CheckboxSelectMultipleSurvey(forms.CheckboxSelectMultiple):
    option_template_name = 'djf_surveys/widgets/checkbox_option.html'


class RadioSelectSurvey(forms.RadioSelect):
    option_template_name = 'djf_surveys/widgets/radio_option.html'


class DateSurvey(forms.DateTimeInput):
    template_name = 'djf_surveys/widgets/datepicker.html'

