from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from django.http import JsonResponse
from django.contrib import messages

from surveys.models import Survey, Question
from surveys.mixin import ContextTitleMixin
from surveys.views import SurveyListView
from surveys.forms import BaseSurveyForm


@method_decorator(staff_member_required, name='dispatch')
class AdminCrateSurveyView(ContextTitleMixin, CreateView):
    model = Survey
    template_name = 'surveys/admins/form.html'
    fields = ['name', 'description']
    title_page = "Add New Survey"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            survey = form.save()
            self.success_url = reverse("surveys:admin_forms_survey", args=[survey.slug])
            messages.success(self.request, f'Successfully {self.title_page}')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(staff_member_required, name='dispatch')
class AdminEditSurveyView(ContextTitleMixin, UpdateView):
    model = Survey
    template_name = 'surveys/admins/form.html'
    fields = ['name', 'description']
    title_page = "Edit Survey"

    def get_success_url(self):
        survey = self.get_object()
        return reverse("surveys:admin_forms_survey", args=[survey.slug])


@method_decorator(staff_member_required, name='dispatch')
class AdminSurveyListView(SurveyListView):
    template_name = 'surveys/admins/survey_list.html'


@method_decorator(staff_member_required, name='dispatch')
class AdminSurveyFormView(ContextTitleMixin, FormMixin, DetailView):
    model = Survey
    template_name = 'surveys/admins/form_preview.html'
    form_class = BaseSurveyForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(survey=self.get_object(), user=self.request.user, **self.get_form_kwargs())

    def get_title_page(self):
        return self.get_object().name

    def get_sub_title_page(self):
        return self.get_object().description


@method_decorator(staff_member_required, name='dispatch')
class AdminCreateQuestionView(ContextTitleMixin, CreateView):
    model = Question
    template_name = 'surveys/admins/form.html'
    success_url = "/"
    fields = ['label', 'type_field', 'choices', 'help_text', 'required']
    title_page = 'Add Question'
    survey = None

    def dispatch(self, request, *args, **kwargs):
        self.survey = get_object_or_404(Survey, id=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = self.survey
            question.save()
            messages.success(self.request, f'Successfully {self.title_page}')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("surveys:admin_forms_survey", args=[self.survey.pk])


@method_decorator(staff_member_required, name='dispatch')
class AdminUpdateQuestionView(ContextTitleMixin, UpdateView):
    model = Question
    template_name = 'surveys/admins/form.html'
    success_url = "/"
    fields = ['label', 'type_field', 'choices', 'help_text', 'required']
    title_page = 'Add Question'
    survey = None

    def dispatch(self, request, *args, **kwargs):
        question = self.get_object()
        self.survey = question.survey
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("surveys:admin_forms_survey", args=[self.survey.pk])


@method_decorator(staff_member_required, name='dispatch')
class AdminDeleteQuestionView(DetailView):
    model = Question
    survey = None

    def dispatch(self, request, *args, **kwargs):
        question = self.get_object()
        self.survey = question.survey
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        question = self.get_object()
        question.delete()
        return redirect("surveys:admin_forms_survey", pk=self.survey.id)


@method_decorator(staff_member_required, name='dispatch')
class AdminChangeOrderQuestionView(View):
    def post(self, request, *args, **kwargs):
        ordering = request.POST['order_question'].split(",")
        for index, question_id in enumerate(ordering):
            if question_id:
                question = Question.objects.get(id=question_id)
                question.ordering = index
                question.save()

        data = {
            'message': 'Success update ordering question'
        }
        return JsonResponse(data, status=200)
