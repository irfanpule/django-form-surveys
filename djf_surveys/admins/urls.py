from django.urls import path
from djf_surveys.admins import views as admin_views


urlpatterns = [
    path('', admin_views.AdminSurveyListView.as_view(), name='admin_survey'),
    path('create/survey/', admin_views.AdminCrateSurveyView.as_view(), name='admin_create_survey'),
    path('edit/survey/<str:slug>/', admin_views.AdminEditSurveyView.as_view(), name='admin_edit_survey'),
    path('delete/survey/<str:slug>/', admin_views.AdminDeleteSurveyView.as_view(), name='admin_delete_survey'),
    path('forms/<str:slug>/', admin_views.AdminSurveyFormView.as_view(), name='admin_forms_survey'),
    path('question/add/<int:pk>/', admin_views.AdminCreateQuestionView.as_view(), name='admin_create_question'),
    path('question/edit/<int:pk>/', admin_views.AdminUpdateQuestionView.as_view(), name='admin_edit_question'),
    path('question/delete/<int:pk>/', admin_views.AdminDeleteQuestionView.as_view(), name='admin_delete_question'),
    path('question/ordering/', admin_views.AdminChangeOrderQuestionView.as_view(), name='admin_change_order_question'),
    path('download/survey/<str:slug>/', admin_views.DownloadResponseSurveyView.as_view(), name='admin_download_survey'),
    path('summary/survey/<str:slug>/', admin_views.SummaryResponseSurveyView.as_view(), name='admin_summary_survey'),
]
