import string


LETTERS_AND_DIGITS = string.ascii_letters + string.digits

MIN_LEN = 1
MAX_LEN = 16
LEN_TO_GENERATE_SHORT_LINK = 6

LINK_ALREADY_USE_ERROR = 'Предложенный вариант короткой ссылки уже существует.'
INVALID_SYMBOL_ERROR = (
    'Разрешено использовать только заглавные, строчные латинские буквы и цифры'
)
LEN_SHORT_ID_ERROR = (
    'Количество символов должно быть не меньше 1 и не больше 16'
)
EMPTY_RESPONSE_ERROR = 'Отсутствует тело запроса'
LINK_NOT_FOUND = 'Указанный id не найден'
URL_FIELD_IS_EMPTY_ERROR = '"url" является обязательным полем!'
INVALID_SYMBOL_API_ERROR = 'Указано недопустимое имя для короткой ссылки'
