from django.urls import path
from surveys import views

app_name = 'surveys'
urlpatterns = [
    path('', views.SurveyListView.as_view(), name='index'),
    path('detail/<int:pk>', views.DetailSurveyView.as_view(), name='detail'),
    path('edit/<int:pk>', views.EditSurveyFormView.as_view(), name='edit'),
    path('create/<int:pk>', views.CreateSurveyFormView.as_view(), name='create'),
    path('delete/<int:pk>', views.DeleteSurveyAnswerView.as_view(), name='delete'),
]
