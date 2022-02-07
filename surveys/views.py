from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from surveys.models import Survey
from surveys.forms import SurveyForm


@method_decorator(login_required, name='dispatch')
class SurveyListView(ListView):
    model = Survey


@method_decorator(login_required, name='dispatch')
class SurveyFormView(FormMixin, DetailView):
    model = Survey
    template_name = 'surveys/form.html'
    form_class = SurveyForm
    success_url = "/"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(survey=self.get_object(), **self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save(user=request.user, editable=True)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
