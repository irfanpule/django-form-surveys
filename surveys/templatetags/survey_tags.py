from django.template import Library

register = Library()

@register.filter(name='addclass')
def addclass(field, class_attr):
    return field.as_widget(attrs={'class': class_attr})


@register.filter(name='get_id_field')
def get_id_field(field):
    parse = field.auto_id.split("_")
    return parse[-1]
