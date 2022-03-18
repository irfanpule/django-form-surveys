from django.utils.safestring import mark_safe


def create_star(active_star: int) -> str:
    inactive_star = 5 - active_star
    elements = ['<div class="flex content-center">']
    for _ in range(int(active_star)):
        elements.append('<i class ="rating__star rating_active"> </i>')
    for _ in range(inactive_star):
        elements.append('<i class ="rating__star rating_inactive"> </i>')
    elements.append('</div>')
    return mark_safe(''.join(elements))
