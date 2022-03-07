from djf_surveys import app_settings


def surveys_context(request):
    context = {
        'get_master_template': app_settings.SURVEY_MASTER_TEMPLATE
    }
    return context
