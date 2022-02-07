from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from surveys.models import Survey, Answer
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

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(survey=self.get_object(), user=self.request.user, **self.get_form_kwargs())


class DetailSurveyView(DetailView):
    model = Survey
    template_name = "surveys/answer_list.html"

    def get_context_data(self, **kwargs):
        users = get_user_model().objects.all()
        objects = []
        for user in users:
            objects.append({
                'create_by': user,
                'answers': Answer.get_answer(survey=self.get_object(), user=user)
            })

        context = super().get_context_data(**kwargs)
        context['objects'] = objects
        return context
