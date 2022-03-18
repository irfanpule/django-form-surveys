from django.template import Library
from django.utils.html import format_html
from django.utils.safestring import mark_safe
register = Library()


@register.filter(name='addclass')
def addclass(field, class_attr):
    return field.as_widget(attrs={'class': class_attr})


@register.filter(name='get_id_field')
def get_id_field(field):
    parse = field.auto_id.split("_")
    return parse[-1]


@register.filter(name='create_star')
def create_star(number):
    active = int(number)
    inactive = 5 - active
    elements = []
    for _ in range(int(number)):
        elements.append('<i class ="rating__star rating_active"> </i>')
    for _ in range(inactive):
        elements.append('<i class ="rating__star rating_inactive"> </i>')

    return mark_safe(''.join(elements))
