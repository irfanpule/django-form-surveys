# Django Form Survey

Django form survey is an application Django to easier create form survey and easy integrated for your project.

![image](https://raw.githubusercontent.com/irfanpule/django-form-surveys/master/docs/screnshots/dashboard-index.png)
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
- `SURVEY_MASTER_TEMPLATE`, `default='surveys/master.html'`, -> `str`: This configuration to change master template using your template. You can set with your template path. Example `SURVEY_MASTER_TEMPLATE = 'mywebsite/master.html'`
    > NB: This config will be work if on your template use block content `{% block content %}` to include or render content of context from view 
  > and your master template must be including or using [Tailwind CSS](https://tailwindcss.com/).
- `SURVEY_USER_PHOTO_PROFILE`, `default=''`, -> `str`: This configuration is used to add a profile photo object that is related to the User model. Example: `SURVEY_USER_PHOTO_PROFILE = 'self.user.profile.photo.url'`
- `SURVEY_FIELD_VALIDATORS`, -> `dict`: This configuration to override max_length of type filed `email, url, text`
  ```python
  # default value of SURVEY_FIELD_VALIDATORS
  SURVEY_FIELD_VALIDATORS = {
      'max_length': {
          'email': 150,
          'text': 250,
          'url': 250
      }
  }
  ```
  ```python
  # example declare in settings.py
  SURVEY_FIELD_VALIDATORS = {
      'max_length': {
          'email': 110,
      }
  }
  ```

## Features
- Manage a survey: You must as superuser to manage survey
    - You can `create, edit, delete` a survey and `show all available survey`.
    - To manage survey you can access `http://localhost:8000/surveys/dashboard/`.
    - ![image](https://raw.githubusercontent.com/irfanpule/django-form-surveys/master/docs/gif/djf_create_survey_edit.gif)
- Option config survey: You can set a survey editable, deletable or duplicate entry
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
    - ![image](https://raw.githubusercontent.com/irfanpule/django-form-surveys/master/docs/gif/djf_type_field_edit.gif)
- Easy sorting question: You can drag and drop to sort question
  - ![image](https://raw.githubusercontent.com/irfanpule/django-form-surveys/master/docs/gif/djf_drag_n_drop_edit.gif)
- Change master template: look section `Configuration`
- Duplicate entry: look section `Configuration`


### Thanks!
![image](https://raw.githubusercontent.com/irfanpule/django-form-surveys/master/docs/gif/djf_submit_survey_edit.gif)
