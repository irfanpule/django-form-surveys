==============
Django Form Surveys
==============

Django form survey is an application Django to easier create form survey and easy integrated for your project.

Quick start
-----------

1. Add "djf_surveys" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'djf_surveys',
    ]

2. Add context processor `'djf_surveys.context_processors.surveys_context'`::

    'context_processors': [
        ....
        'djf_surveys.context_processors.surveys_context'
    ],
3. Run `python manage.py migrate` to create the djf_surveys models.
4. Include url `djf_surveys` in your root url::

    ....

    urlpatterns = [
        path('admin/', admin.site.urls),
        .....
        path('surveys', include('djf_surveys.urls'))
    ]

5. Start the development server and visit `http://127.0.0.1:8000/admin/`
   to create a survey.
6. Access `http://127.0.0.1:8000/surveys/` get list of survey
7. Access `http://127.0.0.1:8000/surveys/{id}` get form of survey
