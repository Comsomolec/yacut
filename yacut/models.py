import random
import re
from datetime import datetime

from flask import url_for
from wtforms.validators import ValidationError

from yacut import db

from .constants import (
    ATTEMPT_COUNT,
    INVALID_SYMBOL_ERROR,
    LETTERS_AND_DIGITS,
    LEN_TO_GENERATE_SHORT_LINK,
    LEN_ORIGINAL_ERROR,
    LEN_SHORT_ERROR,
    LINK_ALREADY_USE_ERROR,
    MAX_ORIGINAL_LINK_LENGHT,
    MAX_SHORT_LINK_LENGHT,
    PATTERN_LINK,
)
from settings import REDIRECT_FROM_SHORT_LINK

class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LINK_LENGHT), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LINK_LENGHT), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                REDIRECT_FROM_SHORT_LINK,
                short_id=self.short,
                _external=True
            )
        )

    @staticmethod
    def get_urlmap(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short_id(len_link=LEN_TO_GENERATE_SHORT_LINK):
        for _ in ATTEMPT_COUNT:
            random_link = ''.join(
                random.choices(LETTERS_AND_DIGITS, k=len_link)
            )
            if URLMap.get_urlmap(short=random_link) is not None:
                continue
            return random_link

    @staticmethod
    def create_urlmap(original, short=None):
        if len(original) > MAX_ORIGINAL_LINK_LENGHT:
            raise ValidationError(LEN_ORIGINAL_ERROR)
        if short is None or short == '':
            short = URLMap.get_unique_short_id()
        else:
            if len(short) > MAX_SHORT_LINK_LENGHT:
                raise ValidationError(LEN_SHORT_ERROR)
            if bool(re.match(PATTERN_LINK, short)):
                raise ValidationError(INVALID_SYMBOL_ERROR)
            if URLMap.get_urlmap(short=short) is not None:
                raise ValidationError(LINK_ALREADY_USE_ERROR)
        url_map = URLMap(
            original=original,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get_urlmap_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404()
