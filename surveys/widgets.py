from django import forms


class CheckboxSelectMultipleSurvey(forms.CheckboxSelectMultiple):
    option_template_name = 'surveys/widgets/checkbox_option.html'


class RadioSelectSurvey(forms.RadioSelect):
    option_template_name = 'surveys/widgets/radio_option.html'
