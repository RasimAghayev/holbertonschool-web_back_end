#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from flask import Flask, jsonify, abort, json, Response, request
from flask_cors import CORS, cross_origin
from api.v1.views import app_views
from typing import Tuple

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
AUTH_TYPE = getenv("AUTH_TYPE")

if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth

    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth

    auth = BasicAuth()


@app.errorhandler(404)
def not_found(error) -> Tuple:
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauth(error) -> Tuple:
    """Unauthorized handler"""
    response = {"error": "Unauthorized"}
    pretty_response = json.dumps(response, indent=2)
    return Response(pretty_response, status=401, mimetype='application/json')


@app.errorhandler(403)
def forbid(error) -> Tuple:
    """Unauthorized handler"""
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request() -> str:
    """Before Request Handler
    Requests Validation
    """
    if auth is None:
        return

    excluded_paths = [
        "/api/v1/status/", "/api/v1/unauthorized/", "/api/v1/forbidden/"
    ]

    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
