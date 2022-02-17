from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from surveys.models import Survey
from surveys.mixin import ContextTitleMixin
from surveys.views import SurveyListView


@method_decorator(staff_member_required, name='dispatch')
class CrateSurveyView(ContextTitleMixin, CreateView):
    model = Survey
    template_name = 'surveys/admins/form.html'
    success_url = "/"
    fields = '__all__'
    title_page = "Add New Survey"


@method_decorator(staff_member_required, name='dispatch')
class AdminSurveyListView(SurveyListView):
    template_name = 'surveys/admins/survey_list.html'
