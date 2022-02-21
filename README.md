# Django Form Survey

Django form survey is an application Django to easier create form survey and easy integrated for your project.

![image](https://raw.githubusercontent.com/irfanpule/django-form-surveys/master/docs/screnshots/dashboard-index.png)

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