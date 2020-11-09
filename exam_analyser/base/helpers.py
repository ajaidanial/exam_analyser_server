import secrets
import string


def is_int(value):
    """Checks if the given value is an integer or not."""

    if type(value) != int and not str(value).isdigit():
        return False
    return True


def random_n_token(n):
    """Generate a random string with numbers and characters with `n` length."""

    allowed_characters = (
        string.ascii_letters + string.digits
    )  # contains char and digits
    return "".join(secrets.choice(allowed_characters) for _ in range(n))
