from .errors import ValidationError


def validate(variable, variable_type, error_message):
    if not isinstance(variable, variable_type):
        raise ValidationError(error_message)
