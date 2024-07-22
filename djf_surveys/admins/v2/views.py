from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import Http404

from djf_surveys.app_settings import SURVEYS_ADMIN_BASE_PATH
from djf_surveys.models import Survey, Question, TYPE_FIELD, TermsValidators
from djf_surveys.mixin import ContextTitleMixin
from djf_surveys.admins.v2.forms import (
    QuestionForm, QuestionWithChoicesForm, QuestionFormRatings, QuestionEmailForm, QuestionTextForm,
    QuestionTextAreaForm, QuestionNumberForm
)
from djf_surveys.validators import TermsEmailValidator, TermsTextValidator, TermsTextAreaValidator, TermsNumberValidator


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
        elif self.type_field_id == TYPE_FIELD.rating:
            return QuestionFormRatings
        elif self.type_field_id == TYPE_FIELD.email:
            return QuestionEmailForm
        elif self.type_field_id == TYPE_FIELD.text:
            return QuestionTextForm
        elif self.type_field_id == TYPE_FIELD.text_area:
            return QuestionTextAreaForm
        elif self.type_field_id == TYPE_FIELD.number:
            return QuestionNumberForm
        else:
            return QuestionForm

    def form_valid(self, form):
        question = form.save(commit=False)
        question.survey = self.survey
        question.type_field = self.type_field_id
        self.object = question.save()

        # save terms validator
        if self.type_field_id == TYPE_FIELD.email:
            terms = TermsEmailValidator(
                type_filter=form.cleaned_data['type_filter'], email_domain=form.cleaned_data['email_domain']
            )
            TermsValidators.objects.create(question=question, terms=terms.to_dict())
        elif self.type_field_id == TYPE_FIELD.text:
            terms = TermsTextValidator(
                min_length=form.cleaned_data['min_length'], max_length=form.cleaned_data['max_length']
            )
            TermsValidators.objects.create(question=question, terms=terms.to_dict())
        elif self.type_field_id == TYPE_FIELD.text_area:
            terms = TermsTextAreaValidator(
                min_length=form.cleaned_data['min_length'], max_length=form.cleaned_data['max_length']
            )
            TermsValidators.objects.create(question=question, terms=terms.to_dict())
        elif self.type_field_id == TYPE_FIELD.number:
            terms = TermsNumberValidator(
                min_value=form.cleaned_data['min_value'], max_value=form.cleaned_data['max_value']
            )
            TermsValidators.objects.create(question=question, terms=terms.to_dict())

        messages.success(self.request, gettext("%(page_action_name)s succeeded.") % dict(
                         page_action_name=capfirst(self.title_page.lower())))
        return super().form_valid(form)

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
        elif self.type_field_id == TYPE_FIELD.rating:
            return QuestionFormRatings
        elif self.type_field_id == TYPE_FIELD.email:
            return QuestionEmailForm
        elif self.type_field_id == TYPE_FIELD.text:
            return QuestionTextForm
        elif self.type_field_id == TYPE_FIELD.text_area:
            return QuestionTextAreaForm
        elif self.type_field_id == TYPE_FIELD.number:
            return QuestionNumberForm
        else:
            return QuestionForm

    def get_object(self):
        object = super(UpdateView, self).get_object(self.get_queryset())
        if object.type_field == TYPE_FIELD.rating:
            if not object.choices:  # use 5 as default for backward compatibility
                object.choices = 5
        return object

    def get_initial(self):
        initial = super().get_initial()

        # initial data for TermsValidators
        if hasattr(self.object, 'termsvalidators'):
            if self.type_field_id == TYPE_FIELD.email:
                terms = TermsEmailValidator.to_object(self.object.termsvalidators.terms)
                initial['type_filter'] = terms.type_filter
                initial['email_domain'] = terms.email_domain
            elif self.type_field_id == TYPE_FIELD.text:
                terms = TermsTextValidator.to_object(self.object.termsvalidators.terms)
                initial['min_length'] = terms.min_length
                initial['max_length'] = terms.max_length
            elif self.type_field_id == TYPE_FIELD.text_area:
                terms = TermsTextAreaValidator.to_object(self.object.termsvalidators.terms)
                initial['min_length'] = terms.min_length
                initial['max_length'] = terms.max_length
            elif self.type_field_id == TYPE_FIELD.number:
                terms = TermsNumberValidator.to_object(self.object.termsvalidators.terms)
                initial['min_value'] = terms.min_value
                initial['max_value'] = terms.max_value
        return initial

    def form_valid(self, form):
        question = form.save(commit=False)
        question.survey = self.survey
        question.type_field = self.type_field_id
        self.object = question.save()

        # save terms validator
        if self.type_field_id == TYPE_FIELD.email:
            terms = TermsEmailValidator(
                type_filter=form.cleaned_data['type_filter'], email_domain=form.cleaned_data['email_domain']
            )
            TermsValidators.objects.update_or_create(
                question=question, defaults={"terms": terms.to_dict(), "question": question})
        elif self.type_field_id == TYPE_FIELD.text:
            terms = TermsTextValidator(
                min_length=form.cleaned_data['min_length'], max_length=form.cleaned_data['max_length']
            )
            TermsValidators.objects.update_or_create(
                question=question, defaults={"terms": terms.to_dict(), "question": question})
        elif self.type_field_id == TYPE_FIELD.text_area:
            terms = TermsTextAreaValidator(
                min_length=form.cleaned_data['min_length'], max_length=form.cleaned_data['max_length']
            )
            TermsValidators.objects.update_or_create(
                question=question, defaults={"terms": terms.to_dict(), "question": question})
        elif self.type_field_id == TYPE_FIELD.number:
            terms = TermsNumberValidator(
                min_value=form.cleaned_data['min_value'], max_value=form.cleaned_data['max_value']
            )
            TermsValidators.objects.update_or_create(
                question=question, defaults={"terms": terms.to_dict(), "question": question})

        messages.success(self.request, gettext("%(page_action_name)s succeeded.") % dict(
                         page_action_name=capfirst(self.title_page.lower())))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_field_id'] = self.type_field_id
        return context

    def get_success_url(self):
        return reverse("djf_surveys:admin_forms_survey", args=[self.survey.slug])

    def get_sub_title_page(self):
        question = self.get_object()
        return gettext("Type Field %s") % question.get_type_field_display()
