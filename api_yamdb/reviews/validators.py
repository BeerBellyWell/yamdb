from django.core.exceptions import ValidationError
import datetime as dt


def validate_year(value):
    year = dt.date.today().year
    if not 0 < value <= year:
        raise ValidationError(
            {'year': "Год неправильный"})
