from http import HTTPStatus

from flask import jsonify, request

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
    url = URLMap.get_urlmap(short_id)
    if url is None:
        raise InvalidAPIUsage(LINK_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({"url": url.original}), HTTPStatus.OK


@app.route("/api/id/", methods=["POST"])
def add_id():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(EMPTY_RESPONSE_ERROR)
    if "url" not in data:
        raise InvalidAPIUsage(URL_FIELD_IS_EMPTY_ERROR)
    try:
        url_map = URLMap.create_urlmap(
            original=data['url'],
            short=data['custom_id']
        )
    except Exception as error:
        raise InvalidAPIUsage(error)
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED
