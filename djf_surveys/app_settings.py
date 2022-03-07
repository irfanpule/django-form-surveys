from django.conf import settings

SURVEY_DUPLICATE_ENTRY = settings.SURVEY_DUPLICATE_ENTRY if hasattr(settings, 'SURVEY_DUPLICATE_ENTRY') else False
SURVEY_MASTER_TEMPLATE = settings.SURVEY_MASTER_TEMPLATE if hasattr(settings,
                                                                    'SURVEY_MASTER_TEMPLATE') else 'djf_surveys/master.html'
SURVEY_USER_PHOTO_PROFILE = settings.SURVEY_USER_PHOTO_PROFILE if hasattr(settings, 'SURVEY_USER_PHOTO_PROFILE') else ""
