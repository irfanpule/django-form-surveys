from django.urls import path
from surveys import views
from surveys.admins import views as admin_views

app_name = 'surveys'
urlpatterns = [
    path('', views.SurveyListView.as_view(), name='index'),
    path('detail/<int:pk>', views.DetailSurveyView.as_view(), name='detail'),
    path('edit/<int:pk>', views.EditSurveyFormView.as_view(), name='edit'),
    path('create/<int:pk>', views.CreateSurveyFormView.as_view(), name='create'),
    path('delete/<int:pk>', views.DeleteSurveyAnswerView.as_view(), name='delete'),
]

urlpatterns += [
    path('dashboard/', admin_views.AdminSurveyListView.as_view(), name='admin_survey'),
    path('dashboard/create/survey/', admin_views.AdminCrateSurveyView.as_view(), name='admin_create_survey'),
    path('dashboard/forms/<int:pk>/', admin_views.AdminSurveyFormView.as_view(), name='admin_forms_survey'),
    path('dashboard/question/add/', admin_views.AdminCreateQuestionView.as_view(), name='admin_create_question'),
]
