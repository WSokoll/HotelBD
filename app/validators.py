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
