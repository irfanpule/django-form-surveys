from typing import List, Tuple

from django.utils.safestring import mark_safe
from djf_surveys.models import Question


def make_choices(question: Question) -> List[Tuple[str, str]]:
    """ to make choices from field question.choices
    """
    choices = []
    for choice in question.choices.split(','):
        choice = choice.strip()
        choices.append((choice.replace(' ', '_').lower(), choice))
    return choices


def create_star(active_star: int) -> str:
    inactive_star = 5 - active_star
    elements = []
    for _ in range(int(active_star)):
        elements.append('<i class ="rating__star rating_active"> </i>')
    for _ in range(inactive_star):
        elements.append('<i class ="rating__star rating_inactive"> </i>')
    return mark_safe(''.join(elements))
