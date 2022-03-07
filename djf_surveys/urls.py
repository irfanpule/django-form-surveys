from django.urls import path
from djf_surveys import views
from djf_surveys.admins import views as admin_views

app_name = 'djf_surveys'
urlpatterns = [
    path('', views.SurveyListView.as_view(), name='index'),
    path('detail/<str:slug>', views.DetailSurveyView.as_view(), name='detail'),
    path('edit/<int:pk>', views.EditSurveyFormView.as_view(), name='edit'),
    path('create/<str:slug>', views.CreateSurveyFormView.as_view(), name='create'),
    path('delete/<int:pk>', views.DeleteSurveyAnswerView.as_view(), name='delete'),
]

urlpatterns += [
    path('dashboard/', admin_views.AdminSurveyListView.as_view(), name='admin_survey'),
    path('dashboard/create/survey/', admin_views.AdminCrateSurveyView.as_view(), name='admin_create_survey'),
    path('dashboard/edit/survey/<str:slug>', admin_views.AdminEditSurveyView.as_view(), name='admin_edit_survey'),
    path('dashboard/delete/survey/<str:slug>', admin_views.AdminDeleteSurveyView.as_view(), name='admin_delete_survey'),
    path('dashboard/forms/<str:slug>/', admin_views.AdminSurveyFormView.as_view(), name='admin_forms_survey'),
    path('dashboard/question/add/<int:pk>',
         admin_views.AdminCreateQuestionView.as_view(), name='admin_create_question'),
    path('dashboard/question/edit/<int:pk>',
         admin_views.AdminUpdateQuestionView.as_view(), name='admin_edit_question'),
    path('dashboard/question/delete/<int:pk>',
         admin_views.AdminDeleteQuestionView.as_view(), name='admin_delete_question'),
    path('dashboard/question/ordering/', admin_views.AdminChangeOrderQuestionView.as_view(),
         name='admin_change_order_question'),
]
