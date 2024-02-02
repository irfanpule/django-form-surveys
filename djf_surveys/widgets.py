from django import forms


class CheckboxSelectMultipleSurvey(forms.CheckboxSelectMultiple):
    option_template_name = 'djf_surveys/widgets/checkbox_option.html'


class RadioSelectSurvey(forms.RadioSelect):
    option_template_name = 'djf_surveys/widgets/radio_option.html'


class DateSurvey(forms.DateTimeInput):
    template_name = 'djf_surveys/widgets/datepicker.html'


class RatingSurvey(forms.HiddenInput):
    template_name = 'djf_surveys/widgets/star_rating.html'
    stars = 8

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['num_ratings'] = self.num_ratings
        return context

class InlineChoiceField(forms.HiddenInput):
    template_name = 'djf_surveys/widgets/inline_choices.html'
    extra = 3

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if context['widget']['value']:
            context['widget']['choice_value'] = [x.strip() for x in context['widget']['value'].split(',')] 
        else:
            context['widget']['choice_value'] = []

        choices_count = len(context['widget']['choice_value'])
        context['widget']['extra'] = range(1 + choices_count, self.extra + 1 + choices_count)
        return context
