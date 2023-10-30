from http import HTTPStatus

from flask import jsonify, request
from wtforms.validators import ValidationError

from . import app
from .constants import (
    LINK_NOT_FOUND,
    URL_FIELD_IS_EMPTY_ERROR,
    EMPTY_RESPONSE_ERROR,
)
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_url(short_id):
    url_map = URLMap.get(short_id)
    if url_map is None:
        raise InvalidAPIUsage(LINK_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({"url": url_map.original}), HTTPStatus.OK


@app.route("/api/id/", methods=["POST"])
def add_id():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(EMPTY_RESPONSE_ERROR)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_FIELD_IS_EMPTY_ERROR)
    try:
        return (
            jsonify(
                URLMap.create(
                    original=data['url'],
                    short=data.get('custom_id'),
                    validation=True
                ).to_dict()
            ),
            HTTPStatus.CREATED
        )
    except (ValidationError, RuntimeError) as error:
        raise InvalidAPIUsage(str(error))
