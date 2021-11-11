from hashlib import sha1

import flask
from flask import Response, make_response, session
from flask.sessions import session_json_serializer
from itsdangerous import URLSafeTimedSerializer

from backend.tests.utility import make_cookie

bp = flask.Blueprint("common_api", __name__, url_prefix="/api/v1/")


@bp.get("/ping")
def ping():
    return "pong", 200, {"content-type": "text/plain"}


@bp.get("/cookie")
def set_cookie():
    session["id"] = '1'
    cookie = make_cookie(id='1')
    return cookie, 200


@bp.get("/decode/<string:cookie>")
def decode_cookie(cookie: str):
    s = URLSafeTimedSerializer(
        'dev', salt='cookie-session',
        serializer=session_json_serializer,
        signer_kwargs={'key_derivation': 'hmac', 'digest_method': sha1}
    )
    response = {
        "arg_decoded": s.loads(cookie),
        "cookie": dict(session),
        # "cookie_decoded": s.loads(session)
    }

    return response, 200, {"content-type": "text/plain"}
