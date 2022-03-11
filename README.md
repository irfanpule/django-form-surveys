# Django Form Survey

Django form survey is an application Django to easier create form survey and easy integrated for your project.

![image](https://raw.githubusercontent.com/irfanpule/django-form-surveys/master/docs/screnshots/dashboard-index.png)

### Installation
- Install django-form-surveys using:
    ```
    pip install django-form-surveys
    ```

- Add `djf_surveys` to your `INSTALLED_APPS` setting like this
    ```
    INSTALLED_APPS = [
        ...
        'djf_surveys',
    ]
    ```

- Add context processor `'djf_surveys.context_processors.surveys_context'`
    ```
    'context_processors': [
        ....
        'djf_surveys.context_processors.surveys_context'
    ],
    ```
- Run `python manage.py migrate` to create the djf_surveys models.
- Include url `djf_surveys` in your root url
    ```
    ....

    urlpatterns = [
        path('admin/', admin.site.urls),
        .....
        path('surveys', include('djf_surveys.urls'))
    ]
    ```
  
- Start the development server and visit `http://127.0.0.1:8000/admin/`
   to create a survey.
- Access `http://127.0.0.1:8000/surveys/` get list of survey 
- Access `http://127.0.0.1:8000/surveys/{id}` get form of survey
- Access `http://127.0.0.1:8000/surveys/dashboard/` to enter admin page