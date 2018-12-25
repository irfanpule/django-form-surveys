from django.shortcuts import render

from surveys.models import Survey
from surveys.forms import SurveyForm


def index(request):
    survey = Survey.objects.last()
    form = SurveyForm(data=request.POST or None, survey=survey)

    if form.is_valid():
        form.save()

    context = {
        'title': survey.name,
        'form': form
    }
    return render(request, 'surveys/index.html', context)
