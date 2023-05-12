import csv
from io import StringIO

from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404

from djf_surveys.app_settings import SURVEYS_ADMIN_BASE_PATH
from djf_surveys.models import Survey, Question, TYPE_FIELD
from djf_surveys.mixin import ContextTitleMixin
from djf_surveys.admins.v2.forms import QuestionForm, QuestionWithChoicesForm


@method_decorator(staff_member_required, name='dispatch')
class AdminCreateQuestionView(ContextTitleMixin, CreateView):
    template_name = 'djf_surveys/admins/question_form_v2.html'
    success_url = reverse_lazy("djf_surveys:")
    title_page = _("Add Question")
    survey = None
    type_field_id = None

    def dispatch(self, request, *args, **kwargs):
        self.survey = get_object_or_404(Survey, id=kwargs['pk'])
        self.type_field_id = kwargs['type_field']
        if self.type_field_id not in TYPE_FIELD:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        choices = [TYPE_FIELD.multi_select, TYPE_FIELD.select, TYPE_FIELD.radio]
        if self.type_field_id in choices:
            return QuestionWithChoicesForm
        else:
            return QuestionForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = self.survey
            question.type_field = self.type_field_id
            question.save()
            messages.success(self.request, gettext("%(page_action_name)s succeeded.") % dict(page_action_name=capfirst(self.title_page.lower())))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_field_id'] = self.type_field_id
        return context

    def get_success_url(self):
        return reverse("djf_surveys:admin_forms_survey", args=[self.survey.slug])

    def get_sub_title_page(self):
        return gettext("Type Field %s") % Question.TYPE_FIELD[self.type_field_id][1]


@method_decorator(staff_member_required, name='dispatch')
class AdminUpdateQuestionView(ContextTitleMixin, UpdateView):
    model = Question
    template_name = 'djf_surveys/admins/question_form_v2.html'
    success_url = SURVEYS_ADMIN_BASE_PATH
    title_page = _("Edit Question")
    survey = None
    type_field_id = None

    def dispatch(self, request, *args, **kwargs):
        question = self.get_object()
        self.type_field_id = question.type_field
        self.survey = question.survey
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        choices = [TYPE_FIELD.multi_select, TYPE_FIELD.select, TYPE_FIELD.radio]
        if self.type_field_id in choices:
            return QuestionWithChoicesForm
        else:
            return QuestionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_field_id'] = self.type_field_id
        return context

    def get_success_url(self):
        return reverse("djf_surveys:admin_forms_survey", args=[self.survey.slug])

    def get_sub_title_page(self):
        question = self.get_object()
        return gettext("Type Field %s") % question.get_type_field_display()
