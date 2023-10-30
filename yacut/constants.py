import string


LETTERS_AND_DIGITS = string.ascii_letters + string.digits
PATTERN_SHORT = fr'^[{(LETTERS_AND_DIGITS)}]*$'

ATTEMPT_COUNT = 100
LEN_TO_GENERATE_SHORT = 6
MAX_ORIGINAL_LINK_LENGHT = 2048
MAX_SHORT_LENGHT = 16

EMPTY_RESPONSE_ERROR = 'Отсутствует тело запроса'
GENERATION_SHORT_ERROR = 'Неудалось автоматически создать короткую ссылку'
INVALID_SYMBOL_ERROR = 'Указано недопустимое имя для короткой ссылки'
SHORT_ALREADY_USE_ERROR = 'Предложенный вариант короткой ссылки уже существует.'
LEN_ORIGINAL_ERROR = (
    f'Ссылка не может превышать {MAX_ORIGINAL_LINK_LENGHT} символов'
)
LEN_SHORT_ERROR = (
    f'Количество символов должно быть не меньше 1 и '
    f'не больше {MAX_SHORT_LENGHT}'
)
LINK_NOT_FOUND = 'Указанный id не найден'
URL_FIELD_IS_EMPTY_ERROR = '"url" является обязательным полем!'
