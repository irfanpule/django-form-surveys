from django.urls import path
from surveys import views, admin_views

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
    path('dashboard/create/survey/', admin_views.CrateSurveyView.as_view(), name='admin_create_survey'),
]
