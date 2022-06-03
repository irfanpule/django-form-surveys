from djf_surveys import app_settings


def surveys_context(request):
    context = {
        'get_master_template': app_settings.SURVEY_MASTER_TEMPLATE,
        'chart_js_src': app_settings.CHART_JS_SRC
    }
    return context
