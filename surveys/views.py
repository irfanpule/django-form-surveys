from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect

from surveys.models import Survey, UserAnswer
from surveys.forms import CreateSurveyForm, EditSurveyForm
from surveys import app_settings


@method_decorator(login_required, name='dispatch')
class SurveyListView(ListView):
    model = Survey


@method_decorator(login_required, name='dispatch')
class SurveyFormView(FormMixin, DetailView):
    template_name = 'surveys/form.html'
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = self.title_page
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')
class CreateSurveyFormView(SurveyFormView):
    model = Survey
    form_class = CreateSurveyForm
    success_url = "/"
    title_page = "Add Survey"

    def dispatch(self, request, *args, **kwargs):
        # handle if user have answer survey
        survey = self.get_object()
        if not app_settings.SURVEY_DUPLICATE_ENTRY and \
                UserAnswer.objects.filter(survey=survey, user=request.user).exists():
            return redirect("surveys:detail", pk=survey.id)
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(survey=self.get_object(), user=self.request.user, **self.get_form_kwargs())


@method_decorator(login_required, name='dispatch')
class EditSurveyFormView(SurveyFormView):
    form_class = EditSurveyForm
    title_page = "Edit Survey"
    model = UserAnswer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = self.title_page
        context['object'] = self.get_object().survey
        return context

    def dispatch(self, request, *args, **kwargs):
        # handle if user not same
        user_answer = self.get_object()
        if user_answer.user != request.user:
            return redirect("surveys:detail", pk=user_answer.survey.id)
        return super(EditSurveyFormView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        user_answer = self.get_object()
        return form_class(user_answer=user_answer, **self.get_form_kwargs())


class DetailSurveyView(DetailView):
    model = Survey
    template_name = "surveys/answer_list.html"

    def get_context_data(self, **kwargs):
        user_answers = UserAnswer.objects.all()
        objects = []
        for ua in user_answers:
            objects.append({
                'id': ua.id,
                'create_by': ua.user,
                'created_at': ua.created_at,
                'answers': ua.answer_set.all()
            })

        context = super().get_context_data(**kwargs)
        context['objects'] = objects
        return context
