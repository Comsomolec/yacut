import random
import re
from datetime import datetime

from flask import url_for
from wtforms.validators import ValidationError

from yacut import db

from .constants import (
    ATTEMPT_COUNT,
    GENERATION_URL_ERROR,
    INVALID_SYMBOL_ERROR,
    LETTERS_AND_DIGITS,
    LEN_TO_GENERATE_SHORT,
    LEN_ORIGINAL_ERROR,
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
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short_id():
        for _ in range(ATTEMPT_COUNT):
            short = ''.join(
                random.choices(
                    LETTERS_AND_DIGITS, k=LEN_TO_GENERATE_SHORT
                )
            )
            if URLMap.get(short=short) is not None:
                continue
            return short
        raise RuntimeError(GENERATION_URL_ERROR)

    @staticmethod
    def create(original, short=None, validation=False):
        if validation and short:
            if len(short) > MAX_SHORT_LINK_LENGHT:
                raise ValidationError(INVALID_SYMBOL_ERROR)
        if not short:
            short = URLMap.get_unique_short_id()
        if validation:
            if len(original) > MAX_ORIGINAL_LINK_LENGHT:
                raise ValidationError(LEN_ORIGINAL_ERROR)
            if not re.match(PATTERN_LINK, short):
                raise ValidationError(INVALID_SYMBOL_ERROR)
            if URLMap.get(short=short) is not None:
                raise ValidationError(LINK_ALREADY_USE_ERROR)
        url_map = URLMap(
            original=original,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404()
