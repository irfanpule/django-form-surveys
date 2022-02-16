=====
Form Survey
=====

Surveys is a simple Django app to conduct Web-based to create survey. You can
create custom survey from django admin.


Quick start
-----------

1. Add "surveys" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'surveys',
    ]

2. Add context processor `'surveys.context_processors.surveys_context'`::

    'context_processors': [
        ....
        'surveys.context_processors.surveys_context'
    ],
3. Run `python manage.py migrate` to create the surveys models.
4. Include url `surveys` in your root url::

    ....

    urlpatterns = [
        path('admin/', admin.site.urls),
        .....
        path('surveys', include('surveys.urls'))
    ]

5. Start the development server and visit `http://127.0.0.1:8000/admin/`
   to create a survey.
6. Access `http://127.0.0.1:8000/surveys/` get list of survey
7. Access `http://127.0.0.1:8000/surveys/{id}` get form of survey
