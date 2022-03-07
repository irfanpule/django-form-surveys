from typing import List, Tuple

from djf_surveys.models import Question


def make_choices(question: Question) -> List[Tuple[str, str]]:
    """ to make choices from field question.choices
    """
    choices = []
    for choice in question.choices.split(','):
        choice = choice.strip()
        choices.append((choice.replace(' ', '_').lower(), choice))
    return choices
