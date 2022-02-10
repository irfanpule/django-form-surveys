from django.conf import settings


SURVEY_DUPLICATE_ENTRY = settings.SURVEY_DUPLICATE_ENTRY if hasattr(settings, 'SURVEY_DUPLICATE_ENTRY') else False
