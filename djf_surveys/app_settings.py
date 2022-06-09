from django.conf import settings

# replace master template
SURVEY_MASTER_TEMPLATE = settings.SURVEY_MASTER_TEMPLATE if hasattr(settings,
                                                                    'SURVEY_MASTER_TEMPLATE') else 'djf_surveys/master.html'

# profile photo path
SURVEY_USER_PHOTO_PROFILE = settings.SURVEY_USER_PHOTO_PROFILE if hasattr(settings, 'SURVEY_USER_PHOTO_PROFILE') else ""

# date input format
DATE_INPUT_FORMAT = settings.DATE_INPUT_FORMAT if hasattr(settings, 'DATE_INPUT_FORMAT') else \
    ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%d/%m/%y', '%d/%m/%Y']

# validators
field_validators = {
    'max_length': {
        'email': 150,
        'text': 250,
        'url': 250
    }
}
if hasattr(settings, 'SURVEY_FIELD_VALIDATORS'):
    max_length = settings.SURVEY_FIELD_VALIDATORS.get('max_length')
    if max_length:
        field_validators['max_length'].update(max_length)
SURVEY_FIELD_VALIDATORS = field_validators

# charjs source
CHART_JS_SRC = settings.CHART_JS_SRC if hasattr(settings, 'CHART_JS_SRC') else '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'

# number of pagination
number_of_pagination = {
    'survey_list': 12,
    'answer_list': 12 
}
if hasattr(settings, 'SURVEY_PAGINATION_NUMBER'):
    survey_list = settings.SURVEY_PAGINATION_NUMBER.get('survey_list')
    if survey_list:
        number_of_pagination['survey_list'] = survey_list
        
    answer_list = settings.SURVEY_PAGINATION_NUMBER.get('answer_list')
    if answer_list:
        number_of_pagination['answer_list'] = answer_list
SURVEY_PAGINATION_NUMBER = number_of_pagination
