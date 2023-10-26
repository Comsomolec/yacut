import string


LETTERS_AND_DIGITS = string.ascii_letters + string.digits

ATTEMPT_COUNT = 100
MAX_ORIGINAL_LINK_LENGHT = 2048
MAX_SHORT_LINK_LENGHT = 16
LEN_TO_GENERATE_SHORT_LINK = 6

PATTERN_LINK = r'^[a-zA-Z0-9]*$'

LINK_ALREADY_USE_ERROR = 'Предложенный вариант короткой ссылки уже существует.'
INVALID_SYMBOL_ERROR = 'Указано недопустимое имя для короткой ссылки'
LEN_ORIGINAL_ERROR = (
    f'Ссылка не может превышать {MAX_ORIGINAL_LINK_LENGHT} символов'
)
LEN_SHORT_ERROR = (
    f'Количество символов должно быть не меньше 1 и '
    f'не больше {MAX_SHORT_LINK_LENGHT}'
)
EMPTY_RESPONSE_ERROR = 'Отсутствует тело запроса'
LINK_NOT_FOUND = 'Указанный id не найден'
URL_FIELD_IS_EMPTY_ERROR = '"url" является обязательным полем!'
