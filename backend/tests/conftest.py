import random
import string


def generate_random_str(length: int = 10) -> str:
    """Generate a random string of lowercase letters."""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


def generate_random_int(min_value: int = 1, max_value: int = 100) -> int:
    """Generate a random integer between min_value and max_value included."""
    return random.randint(min_value, max_value)
