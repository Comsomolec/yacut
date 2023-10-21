from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from .constants import (
    LETTERS_AND_DIGITS,
    LEN_SHORT_ID_ERROR,
    LINK_ALREADY_USE_ERROR,
    INVALID_SYMBOL_ERROR,
    MIN_LEN,
    MAX_LEN
)
from .models import URLMap


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'), ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(
                min=MIN_LEN,
                max=MAX_LEN,
                message=LEN_SHORT_ID_ERROR
            ),
        ]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(form, field):
        data = field.data
        for symbol in data:
            if symbol not in LETTERS_AND_DIGITS:
                raise ValidationError(message=INVALID_SYMBOL_ERROR)
        if URLMap.query.filter_by(short=data).first() is not None:
            raise ValidationError(message=LINK_ALREADY_USE_ERROR)
        return data
