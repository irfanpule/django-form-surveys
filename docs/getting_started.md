# Getting started

### Requirements
- Python 3.6, 3.8 or latest
- Django 2.2.x or latest

Surveys is a simple Django app to conduct Web-based to create survey. You can
create custom survey from django admin.


### Installation
- Install django-form-surveys using:
    ```
    pip install .....
    ```
    or download release file `tar.gz` and then 
    ```
    pip install ......tar.gz
    ```

- Add `surveys` to your `INSTALLED_APPS` setting like this
    ```
    INSTALLED_APPS = [
        ...
        'surveys',
    ]
    ```

- Add context processor `'surveys.context_processors.surveys_context'`
    ```
    'context_processors': [
        ....
        'surveys.context_processors.surveys_context'
    ],
    ```
- Run `python manage.py migrate` to create the surveys models.
- Include url `surveys` in your root url
    ```
    ....

    urlpatterns = [
        path('admin/', admin.site.urls),
        .....
        path('surveys', include('surveys.urls'))
    ]
    ```
  
- Start the development server and visit `http://127.0.0.1:8000/admin/`
   to create a survey.
- Access `http://127.0.0.1:8000/surveys/` get list of survey 
- Access `http://127.0.0.1:8000/surveys/{id}` get form of survey


### Configuration
There are several configurations that you can write on `settings.py`
- `SURVEY_DUPLICATE_ENTRY`, `default=False` -> `bool`: This configuration can you set `True` to allowed user re-entry on the same survey.
  - `SURVEY_MASTER_TEMPLATE`, `default='surveys/master.html'`, -> `str`: This configuration to change master template using your template. You can set with your template path.
      > NB: this config will be work if on your template use block content `{% block content %}` to include or render content of context from view.