from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp,
    ValidationError
)

from .constants import (
    LEN_SHORT_ERROR,
    INVALID_SYMBOL_ERROR,
    LEN_TO_GENERATE_SHORT,
    LINK_ALREADY_USE_ERROR,
    PATTERN_LINK
)
from .models import URLMap


ORIGINAL_LINK_DESCRIPTION = 'Длинная ссылка'
ORIGINAL_LINK_VALIDATORS_MESSAGE = 'Обязательное поле'
SHORT_LINK_DESCRIPTION = 'Ваш вариант короткой ссылки'
CREATE_LINK_DESCRIPTION = 'Создать'


class URLMapForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_DESCRIPTION,
        validators=[DataRequired(message=ORIGINAL_LINK_VALIDATORS_MESSAGE), ]
    )
    custom_id = StringField(
        SHORT_LINK_DESCRIPTION,
        validators=[
            Optional(),
            Length(
                max=LEN_TO_GENERATE_SHORT,
                message=LEN_SHORT_ERROR
            ),
            Regexp(PATTERN_LINK, message=INVALID_SYMBOL_ERROR)
        ]
    )
    submit = SubmitField(CREATE_LINK_DESCRIPTION)

    def validate_custom_id(form, field):
        if URLMap.get(short=field.data) is not None:
            raise ValidationError(message=LINK_ALREADY_USE_ERROR)
        return field.data
