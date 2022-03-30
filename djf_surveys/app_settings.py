from django.conf import settings

SURVEY_MASTER_TEMPLATE = settings.SURVEY_MASTER_TEMPLATE if hasattr(settings,
                                                                    'SURVEY_MASTER_TEMPLATE') else 'djf_surveys/master.html'
SURVEY_USER_PHOTO_PROFILE = settings.SURVEY_USER_PHOTO_PROFILE if hasattr(settings, 'SURVEY_USER_PHOTO_PROFILE') else ""

DATE_INPUT_FORMAT = settings.DATE_INPUT_FORMAT if hasattr(settings, 'DATE_INPUT_FORMAT') else \
    ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%d/%m/%y', '%d/%m/%Y']

