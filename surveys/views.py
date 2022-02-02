from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import DetailView

from surveys.models import Survey
from surveys.forms import SurveyForm


class SurveyListView(ListView):
    model = Survey
    paginate_by = 20


class SurveyFormView(FormMixin, DetailView):
    model = Survey
    template_name = 'surveys/form.html'
    form_class = SurveyForm

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(survey=self.get_object(), **self.get_form_kwargs())


def detail(request):
    survey = Survey.objects.last()
    form = SurveyForm(data=request.POST or None, survey=survey)

    if form.is_valid():
        form.save()

    context = {
        'title': survey.name,
        'form': form
    }
    return render(request, 'surveys/index.html', context)
