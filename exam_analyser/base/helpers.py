def is_int(value):
    """Checks if the given value is an integer or not."""

    if type(value) != int and not str(value).isdigit():
        return False
    return True
