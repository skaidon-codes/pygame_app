from pygame import Color
from random import randint


def get_random_color(min_value=0, max_value=255):
    return Color(randint(min_value, max_value),
                 randint(min_value, max_value),
                 randint(min_value, max_value))
