from django import forms
from django.utils.translation import gettext_lazy as _
from djf_surveys.models import Question, Survey
from djf_surveys.widgets import InlineChoiceField
from tinymce.widgets import TinyMCE
from djf_surveys.app_settings import SURVEY_TINYMCE_DEFAULT_CONFIG


class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ['label', 'key', 'help_text', 'required']


class QuestionWithChoicesForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ['label', 'key', 'choices', 'help_text', 'required']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choices'].widget = InlineChoiceField()
        self.fields['choices'].help_text = _("Click Button Add to adding choice")


class QuestionFormRatings(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ['label', 'key', 'choices', 'help_text', 'required']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choices'].widget = forms.NumberInput(attrs={'max':10, 'min':1})
        self.fields['choices'].help_text = _("Must be between 1 and 10")
        self.fields['choices'].label = _("Number of ratings")
        self.fields['choices'].initial = 5


class QuestionEmailForm(forms.ModelForm):
    type_filter = forms.ChoiceField(
        label=_("Type Filter"),
        choices=(
            ('', _('--- Choices ---')),
            ('whitelist', 'Whitelist'),
            ('blacklist', 'Blacklist'),
        ),
        widget=forms.Select(),
        required=False,
        help_text=_("Filter type to accept allowed email domains"),
    )
    email_domain = forms.CharField(
        label='Email Domains', help_text=_('Click Button Add to adding data'),
        widget=InlineChoiceField()
    )

    class Meta:
        model = Question
        fields = ['label', 'key', 'help_text', 'required', 'type_filter', 'email_domain']


class SurveyForm(forms.ModelForm):
    
    class Meta:
        model = Survey
        fields = [
            'name', 'slug', 'description', 'editable', 'deletable',
            'duplicate_entry', 'private_response', 'can_anonymous_user',
            'notification_to', 'success_page_content'
        ]
        widgets = {
            'success_page_content': TinyMCE(mce_attrs=SURVEY_TINYMCE_DEFAULT_CONFIG)
        }
        help_texts = {
            'slug': _("Leave the field blank if you want the slug to be generated automatically"),
        }

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if self.instance and self.instance.slug != slug and Survey.objects.filter(slug=slug).exists():
            raise forms.ValidationError(_('Slug already exists'))
        if not self.instance and slug and Survey.objects.filter(slug=slug).exists():
            raise forms.ValidationError(_('Slug already exists'))
        return slug

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notification_to'].widget = InlineChoiceField()
        self.fields['slug'].required = False
