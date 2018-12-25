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

2. Run `python manage.py migrate` to create the surveys models.

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a survey.
