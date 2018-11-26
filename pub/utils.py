from string import ascii_letters, digits
from random import SystemRandom


def get_random_hash(size=32):
    return ''.join(SystemRandom().choices(ascii_letters + digits, k=size))
