from django.urls import path
from surveys import views

app_name = 'surveys'
urlpatterns = [
    path('', views.SurveyListView.as_view(), name='index'),
    path('<int:pk>', views.SurveyFormView.as_view(), name='detail')
]
