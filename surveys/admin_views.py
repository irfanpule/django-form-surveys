from django.views.generic.edit import CreateView
from surveys.models import Survey
from surveys.mixin import ContextTitleMixin


class CrateSurveyView(ContextTitleMixin, CreateView):
    model = Survey
    template_name = 'surveys/form.html'
    success_url = "/"
    fields = '__all__'
    title_page = "Add New Survey"
