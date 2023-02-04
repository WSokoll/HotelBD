from datetime import datetime

from wtforms import ValidationError


class AfterStartValidator:
    """Validates that end date is after start date.
    :param message: error message
     """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if field.data < form.start_date.data:
            raise ValidationError(
                self.message
                or field.gettext(
                    "The end date should be after start date."
                )
            )


class NotPastValidator:
    """Validates that date is not from the past.
    :param message: error message
     """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if field.data < datetime.date(datetime.now()):
            raise ValidationError(
                self.message
                or field.gettext(
                    "The date cannot be in the past."
                )
            )
