from django import forms
from djf_surveys.models import Question


class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ['label', 'key', 'choices', 'help_text', 'required']
