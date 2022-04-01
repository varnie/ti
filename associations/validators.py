import pycountry
from django.core.exceptions import ValidationError


def validate_country_name(val):
    country = pycountry.countries.get(name=val)
    if country is None:
        raise ValidationError(
            f'{val} is not a valid country name',
            params={'value': val},
        )


def validate_currency_alpha3(val):
    currency = pycountry.currencies.get(alpha_3=val)
    if currency is None:
        raise ValidationError(
            f'{val} is not a valid country name',
            params={'value': val},
        )
