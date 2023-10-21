from flask import jsonify, request

from . import app, db
from .constants import (
    LINK_NOT_FOUND,
    URL_FIELD_IS_EMPTY_ERROR,
    EMPTY_RESPONSE_ERROR,
    LETTERS_AND_DIGITS,
    INVALID_SYMBOL_API_ERROR,
    LINK_ALREADY_USE_ERROR,
    MAX_LEN,
)
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage(LINK_NOT_FOUND, 404)
    return jsonify({"url": url.original}), 200


@app.route("/api/id/", methods=["POST"])
def add_id():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(EMPTY_RESPONSE_ERROR)
    if "url" not in data:
        raise InvalidAPIUsage(URL_FIELD_IS_EMPTY_ERROR)
    if (
        ("custom_id" not in data)
        or (data["custom_id"] is None)
        or (data["custom_id"] == "")
    ):
        data["custom_id"] = get_unique_short_id()
    else:
        short_id = data["custom_id"]
        if len(short_id) > MAX_LEN:
            raise InvalidAPIUsage(INVALID_SYMBOL_API_ERROR)
        for symbol in short_id:
            if symbol not in LETTERS_AND_DIGITS:
                raise InvalidAPIUsage(INVALID_SYMBOL_API_ERROR)
        if URLMap.query.filter_by(short=short_id).first() is not None:
            raise InvalidAPIUsage(LINK_ALREADY_USE_ERROR)
    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), 201
