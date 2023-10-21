from random import choice

from .constants import LETTERS_AND_DIGITS, LEN_TO_GENERATE_SHORT_LINK
from .models import URLMap


def get_unique_short_id(len_link=None):
    len_link = LEN_TO_GENERATE_SHORT_LINK if len_link is None else len_link
    while True:
        random_link = ''.join(
            choice(LETTERS_AND_DIGITS) for _ in range(len_link)
        )
        if URLMap.query.filter_by(short=random_link).first():
            continue
        return random_link
