from functools import wraps

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_multiple_of(multiple):
    def validate_multiple(value):
        if value % multiple != 0:
            raise ValidationError(
                _("%(value)s is not a multiple of %(multiple)s"),
                params={"value": value, "multiple": multiple},
            )

    return wraps(validate_multiple_of)(validate_multiple)
