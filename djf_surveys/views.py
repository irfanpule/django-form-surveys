from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib import messages

from djf_surveys.models import Survey, UserAnswer
from djf_surveys.forms import CreateSurveyForm, EditSurveyForm
from djf_surveys.mixin import ContextTitleMixin
from djf_surveys import app_settings
from djf_surveys.utils import NewPaginator


@method_decorator(login_required, name='dispatch')
class SurveyListView(ContextTitleMixin, ListView):
    model = Survey
    title_page = 'Survey List'
    paginate_by = app_settings.SURVEY_PAGINATION_NUMBER['survey_list']
    paginator_class = NewPaginator

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(name__icontains=query)
        else:
            object_list = self.model.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        page_number = self.request.GET.get('page', 1)
        context = super().get_context_data(**kwargs)
        page_range = context['page_obj'].paginator.get_elided_page_range(number=page_number)
        context['page_range'] = page_range
        return context


class SurveyFormView(FormMixin, DetailView):
    template_name = 'djf_surveys/form.html'
    success_url = "/"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()
        if form.is_valid():
            form.save()
            messages.success(self.request, f'Successfully {self.title_page}')
            return self.form_valid(form)
        else:
            messages.error(self.request, 'Something wrong')
            return self.form_invalid(form)


class CreateSurveyFormView(ContextTitleMixin, SurveyFormView):
    model = Survey
    form_class = CreateSurveyForm
    success_url = "/"
    title_page = "Add Survey"

    def dispatch(self, request, *args, **kwargs):
        survey = self.get_object()
        # handle if survey can_anonymous_user
        if not request.user.is_authenticated and not survey.can_anonymous_user:
            messages.warning(request, 'Sorry, you must be logged in to fill out the survey')
            return redirect("/")

        # handle if user have answer survey
        if request.user.is_authenticated and not survey.duplicate_entry and \
                UserAnswer.objects.filter(survey=survey, user=request.user).exists():
            messages.warning(request, 'You have submitted out this survey')
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(survey=self.get_object(), user=self.request.user, **self.get_form_kwargs())

    def get_title_page(self):
        return self.get_object().name

    def get_sub_title_page(self):
        return self.get_object().description


@method_decorator(login_required, name='dispatch')
class EditSurveyFormView(ContextTitleMixin, SurveyFormView):
    form_class = EditSurveyForm
    title_page = "Edit Survey"
    model = UserAnswer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object().survey
        return context

    def dispatch(self, request, *args, **kwargs):
        # handle if user not same
        user_answer = self.get_object()
        if user_answer.user != request.user or not user_answer.survey.editable:
            messages.warning(request, "You can't edit this survey. You don't have permission")
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        user_answer = self.get_object()
        return form_class(user_answer=user_answer, **self.get_form_kwargs())

    def get_title_page(self):
        return self.get_object().survey.name

    def get_sub_title_page(self):
        return self.get_object().survey.description


@method_decorator(login_required, name='dispatch')
class DeleteSurveyAnswerView(DetailView):
    model = UserAnswer

    def dispatch(self, request, *args, **kwargs):
        # handle if user not same
        user_answer = self.get_object()
        if user_answer.user != request.user or not user_answer.survey.deletable:
            messages.warning(request, "You can't delete this survey. You don't have permission")
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user_answer = self.get_object()
        user_answer.delete()
        messages.success(self.request, 'Successfully deleted one survey')
        return redirect("djf_surveys:detail", slug=user_answer.survey.slug)


class DetailSurveyView(ContextTitleMixin, DetailView):
    model = Survey
    template_name = "djf_surveys/answer_list.html"
    title_page = "Result Survey"
    paginate_by = app_settings.SURVEY_PAGINATION_NUMBER['answer_list']

    def dispatch(self, request, *args, **kwargs):
        survey = self.get_object()
        if not self.request.user.is_superuser and survey.private_response:
            messages.warning(request, "You can't access this page")
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user_answers = UserAnswer.objects.filter(survey=self.get_object()) \
            .select_related('user').prefetch_related('answer_set__question')
        paginator = NewPaginator(user_answers, self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        page_range = paginator.get_elided_page_range(number=page_number)
        context = super().get_context_data(**kwargs)
        context['page_obj'] = page_obj
        context['page_range'] = page_range
        return context


@method_decorator(login_required, name='dispatch')
class DetailResultSurveyView(ContextTitleMixin, DetailView):
    title_page = "Detail Result"
    template_name = "djf_surveys/detail_result.html"
    model = UserAnswer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        context['on_detail'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        # handle if user not same
        user_answer = self.get_object()
        if user_answer.user != request.user:
            messages.warning(request, "You can't this. You don't have permission")
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)

    def get_title_page(self):
        return self.get_object().survey.name

    def get_sub_title_page(self):
        return self.get_object().survey.description
