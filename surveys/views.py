from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from surveys.models import Survey, Answer, UserAnswer
from surveys.forms import CreateSurveyForm, EditSurveyForm


@method_decorator(login_required, name='dispatch')
class SurveyListView(ListView):
    model = Survey


@method_decorator(login_required, name='dispatch')
class CreateSurveyFormView(FormMixin, DetailView):
    model = Survey
    template_name = 'surveys/form.html'
    form_class = CreateSurveyForm
    success_url = "/"
    title_page = "Add Survey"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = self.title_page
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(survey=self.get_object(), **self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save(user=request.user)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')
class EditSurveyFormView(CreateSurveyFormView):
    form_class = EditSurveyForm
    title_page = "Edit Survey"
    model = UserAnswer

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        user_answer = self.get_object()
        return form_class(survey=user_answer.survey, user=user_answer.user, **self.get_form_kwargs())


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
                'answers': Answer.get_answer(survey=ua.survey, user=ua.user)
            })

        context = super().get_context_data(**kwargs)
        context['objects'] = objects
        return context
