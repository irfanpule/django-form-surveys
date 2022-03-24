# Django Form Survey

Django form survey is an application Django to easier create form survey and easy integrated for your project.


## Table of content
- Installation
- Configuration
- Features
 
## Installation
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
- Run `python manage.py collectstatic` to collect file static djf_surveys into project.
- Include url `djf_surveys` in your root url
    ```
    ....

    urlpatterns = [
        path('admin/', admin.site.urls),
        .....
        path('surveys/', include('djf_surveys.urls'))
    ]
    ```
  
- Access `http://127.0.0.1:8000/surveys/dashboard/` to enter admin page to create a survey.
- Access `http://127.0.0.1:8000/surveys/` get list of survey 
- Access `http://127.0.0.1:8000/surveys/{id}` get form of survey

## Configuration
There are several configurations that you can write on `settings.py`
- `SURVEY_DUPLICATE_ENTRY`, `default=False` -> `bool`: This configuration can you set `True` to allowed user re-entry on the same survey. Example `SURVEY_DUPLICATE_ENTRY = True`
- `SURVEY_MASTER_TEMPLATE`, `default='surveys/master.html'`, -> `str`: This configuration to change master template using your template. You can set with your template path. Example `SURVEY_MASTER_TEMPLATE = 'mywebsite/master.html'`
    > NB: This config will be work if on your template use block content `{% block content %}` to include or render content of context from view 
  > and your master template must be including or using [Tailwind CSS](https://tailwindcss.com/).
- `SURVEY_USER_PHOTO_PROFILE`, `default=''`, -> `str`: This configuration is used to add a profile photo object that is related to the User model. Example: `SURVEY_USER_PHOTO_PROFILE = 'self.user.profile.photo.url'`

## Features
- Manage a survey: You must as superuser to manage survey
    - You can `create, edit, delete` a survey and `show all available survey`.
    - To manage survey you can access `http://localhost:8000/surveys/dashboard/`.
- Support many question type (type field): Available field types include:
    - Text 
    - Number
    - Radio 
    - Select 
    - Multi Select 
    - Text Area 
    - URL 
    - Email 
    - Date 
    - Rating
    
- Easy sorting question: You can drag and drop to sort question
- Change master template: look section `Configuration`
- Duplicate entry: look section `Configuration`


### Thanks!
