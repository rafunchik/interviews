import string
from random import *


def generate_url(_, length=10):
    """ Generate a random alphanumeric string of give length (default 10 chars)

    :param _: string, not used currently
    :param length: int
    :return: random string
    """
    alphanumeric = string.ascii_letters + string.digits
    return "".join(choice(alphanumeric) for _ in range(length))
