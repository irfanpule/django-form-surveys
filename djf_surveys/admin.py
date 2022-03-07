from django.contrib import admin
from .models import Survey, Question, Answer, UserAnswer


class AdminQuestion(admin.ModelAdmin):
    list_display = ('survey', 'label', 'type_field', 'help_text', 'required')
    search_fields = ('survey', )


class AdminAnswer(admin.ModelAdmin):
    list_display = ('question', 'get_label', 'value', 'user_answer')
    search_fields = ('question__label', 'value',)
    list_filter = ('question__survey',)

    def get_label(self, obj):
        return obj.question.label
    get_label.admin_order_field = 'question'
    get_label.short_description = 'Label'


class AdminUserAnswer(admin.ModelAdmin):
    list_display = ('survey', 'user', 'created_at', 'updated_at')


class AdminSurvey(admin.ModelAdmin):
    list_display = ('name', 'slug')
    exclude = ['slug']


admin.site.register(Survey, AdminSurvey)
admin.site.register(Question, AdminQuestion)
admin.site.register(Answer, AdminAnswer)
admin.site.register(UserAnswer, AdminUserAnswer)
