from .errors import ValidationError


def validate(variable, variable_type, error_message):
    """validate whether variable is the same type as variable_type

    Args:
        variable (Any): variable to check type
        variable_type (Any): type that variable is suppose to be
        error_message (string): [description]

    Raises:
        ValidationError: [description]
    """
    if not isinstance(variable, variable_type):
        raise ValidationError(error_message)
