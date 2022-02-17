from django.views.generic.edit import CreateView
from surveys.models import Survey


class CrateSurveyView(CreateView):
    model = Survey
    template_name = 'surveys/form.html'
    success_url = "/"
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = "Add New Survey"
        return context
