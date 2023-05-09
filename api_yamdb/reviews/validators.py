import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    year = dt.date.today().year
    if not 0 < value <= year:
        raise ValidationError(
            {'year': "Год неправильный"})
