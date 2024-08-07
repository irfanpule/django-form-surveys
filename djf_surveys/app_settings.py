from django.conf import settings

# replace master template
SURVEY_MASTER_TEMPLATE = settings.SURVEY_MASTER_TEMPLATE \
    if hasattr(settings, "SURVEY_MASTER_TEMPLATE") else 'djf_surveys/master.html'

# profile photo path
SURVEY_USER_PHOTO_PROFILE = settings.SURVEY_USER_PHOTO_PROFILE \
    if hasattr(settings, 'SURVEY_USER_PHOTO_PROFILE') else ""

# date input format
DATE_INPUT_FORMAT = settings.DATE_INPUT_FORMAT if hasattr(settings, 'DATE_INPUT_FORMAT') else \
    ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%d/%m/%y', '%d/%m/%Y']

# validators
field_validators = {
    'max_length': {
        'email': 150,
        'text': 250,
        'url': 250,
        'text_area': 1000,
    },
    'min_length': {
        'text_area': 100,
        'text': 3
    }
}
if hasattr(settings, 'SURVEY_FIELD_VALIDATORS'):
    max_length = settings.SURVEY_FIELD_VALIDATORS.get('max_length')
    if max_length:
        field_validators['max_length'].update(max_length)
    min_length = settings.SURVEY_FIELD_VALIDATORS.get("min_length")
    if min_length:
        field_validators['min_length'].update(min_length)

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

# override group url for admin
SURVEYS_ADMIN_BASE_PATH = "dashboard/"

# allow anonymous view of survey list
SURVEY_ANONYMOUS_VIEW_LIST = settings.SURVEY_ANONYMOUS_VIEW_LIST \
    if hasattr(settings, 'SURVEY_ANONYMOUS_VIEW_LIST') else False

# email address which the notification is sent
SURVEY_EMAIL_FROM = settings.SURVEY_EMAIL_FROM \
    if hasattr(settings, 'SURVEY_EMAIL_FROM') else False

# to set link back button on success page
SURVEY_LINK_BACK_ON_SUCCESS_PAGE = settings.SURVEY_LINK_BACK_ON_SUCCESS_PAGE \
    if hasattr(settings, 'SURVEY_LINK_BACK_ON_SUCCESS_PAGE') else "/"


# to set tinymce default config
SURVEY_TINYMCE_DEFAULT_CONFIG = settings.TINYMCE_DEFAULT_CONFIG \
    if hasattr(settings, 'TINYMCE_DEFAULT_CONFIG') else {
    "menubar": "edit view insert format tools table",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
}
