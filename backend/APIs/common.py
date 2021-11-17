import os
from hashlib import sha1

import flask
from flask import session
from flask.sessions import session_json_serializer
from itsdangerous import URLSafeTimedSerializer

bp = flask.Blueprint("util_api", __name__, url_prefix="/api/v1/")

@bp.get("/ping")
def ping():
    return "pong", 200, {"content-type": "text/plain"}


# development only methods
if os.getenv("FLASK_ENV", "development") == "development":
    from backend.tests.utility import make_cookie

    @bp.get("/gen_cookie/<int:user_id>")
    def gen_cookie(user_id: int):
        session["id"] = '1'
        cookie = make_cookie(id=user_id)
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
