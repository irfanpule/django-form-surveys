# Django Form Survey

Django form survey is an application Django to easier create form survey and easy integrated for your project.

![image](https://raw.githubusercontent.com/irfanpule/django-form-surveys/master/docs/gif/djf_submit_survey_edit.gif)

## Table of content
- [Installation](#installation)
- [Features](#features)
    - [Manage Surveys](#manage-a-survey)
    - [Option Config](#option-survey)
    - [Question Types](#questioin-type)
    - [Easy Sort](#easy-sorting-question)
    - [Summary Respondents](#summary)
    - [Download Report](#download-report)
    - [Notification](#notification)
- [Configuration](#configuration)
    - [Change Master Template](#change-master-template)
    - [User Photo Profile](#user-photo-profile)
    - [Field Validators](#field-validators)
    - [Email From](#email-from)
    - [Anonymous Access](#anonymous-access-surveys)
    - [Link Back Button On Succes Page](#link-back-button-on-success-page)
- [For Contributor](#for-contributor)


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
          'tinymce',  # dependency
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


## Features
#### Manage a Survey
You must as superuser to manage survey. You can `create, edit, delete, search and show all available survey`. To manage survey you can access `http://localhost:8000/surveys/dashboard/`.
      ![image](https://raw.githubusercontent.com/irfanpule/django-form-surveys/master/docs/gif/djf_create_survey_edit.gif)

#### Option Survey
You can use the options below
- `editable`: this option allows the user to edit the answer
- `deletable`: this option allows the user to delete the answer
- `duplicate entry`: this option allows users to submit more than once
- `private reponse`: this option makes the answer list only visible to admin
- `can anonymous user`: This option allows users without authentication to submit

#### Questioin Type
Available field types include:
![image](https://user-images.githubusercontent.com/11069520/237864026-9f933369-4cf0-4292-a394-ac398eb1be9b.png)
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

#### Easy Sorting Question
You can drag and drop to sort question
  ![image](https://raw.githubusercontent.com/irfanpule/django-form-surveys/master/docs/gif/djf_drag_n_drop_edit.gif)

#### Summary
You can see the survey summary in a charts. Summary just calculate type field "radio, select, multi_select, rating"
  ![summary](https://raw.githubusercontent.com/irfanpule/django-form-surveys/master/docs/screnshots/chart_summary.png)

#### Download Report
You can download report as csv

#### Notification
You can send an email notification when the survey is submitted. To make sure it works look section `Configuration`
![notification](https://raw.githubusercontent.com/irfanpule/django-form-surveys/master/docs/screnshots/notification_to.png)

### Success Page Content
You can change the content of the success page to provide specific instructions or a special message.
![success_page](https://raw.githubusercontent.com/irfanpule/django-form-surveys/master/docs/screnshots/success-page.png)
![success_page](https://raw.githubusercontent.com/irfanpule/django-form-surveys/master/docs/screnshots/success-page-content.png)
This use `django-tinycme`. For advanced config toolbar you can see the [Documentation](https://django-tinymce.readthedocs.io/en/latest/index.html)



### Configuration
There are several configurations that you can write on `settings.py`

#### Change Master Template
`SURVEY_MASTER_TEMPLATE`, `default='surveys/master.html'`, -> `str`: This configuration to change master template using your template. You can set with your template path. Example `SURVEY_MASTER_TEMPLATE = 'mywebsite/master.html'`
    > NB: This config will be work if on your template use block content `{% block content %}` to include or render content of context from view 
  > and your master template must be including or using [Tailwind CSS](https://tailwindcss.com/).

#### User Photo Profile
`SURVEY_USER_PHOTO_PROFILE`, `default=''`, -> `str`: This configuration is used to add a profile photo object that is related to the User model. Example: `SURVEY_USER_PHOTO_PROFILE = 'self.user.profile.photo.url'`

#### Field Validators
`SURVEY_FIELD_VALIDATORS`, -> `dict`: This configuration to override max_length of type filed `email, url, text` and min_length of type filed `text_area, text`
```python
# default value of SURVEY_FIELD_VALIDATORS
SURVEY_FIELD_VALIDATORS = {
    'max_length': {
        'email': 150,
        'text': 250,
        'url': 250,
        'text_area': 1000
    },
    'min_length': {
        'text_area': 100,
        'text': 3
    }
}
```
```python
# example declare in settings.py
SURVEY_FIELD_VALIDATORS = {
    'max_length': {
        'email': 110,
    },
    'min_length': {
      'text_area': 50,
    }
}
```

#### Number of Pagination
`SURVEY_PAGINATION_NUMBER`, -> `dict`: This configuration to override number of pagination `survey_list` and `answer_list`
```python
# example override in settings.py
# default value 12
SURVEY_PAGINATION_NUMBER = {
    'answer_list': 3,
    'survey_list': 2
}
```

#### Email From
#### Email From
`SURVEY_EMAIL_FROM`, -> `str`: Enter your email from and then don't forget to define your SMTP

#### Anonymous Access Surveys
`SURVEY_ANONYMOUS_VIEW_LIST`, -> `bool`: This configuration allows anonymous access to the survey page. The survey that appears has an `Anonymous submission` option.


#### Link Back Button On Success Page
`SURVEY_LINK_BACK_ON_SUCCESS_PAGE` -> `str`: This configuration is to change default link back on success page
## For Contributor
- clone project
- symlink app to `demo`
  ```bash
  ln -s [path_project_djf_survey] [path_demo_djf_survey]
  ```
- create `env` development
- active `env`
- enter directory `demo`
- now, you can access all command `manage.py`
