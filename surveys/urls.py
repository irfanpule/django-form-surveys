from django.urls import path
from surveys import views

appp_name = 'surveys'
urlpatterns = [
    path('', views.index, name='index')
]
