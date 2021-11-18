from hashlib import sha1

from flask.sessions import session_json_serializer
from itsdangerous import URLSafeTimedSerializer

from backend.tests import conftest


def make_cookie(**kwargs) -> str:
    s = URLSafeTimedSerializer(
        conftest.SECRET_KEY, salt='cookie-session',
        serializer=session_json_serializer,
        signer_kwargs={'key_derivation': 'hmac', 'digest_method': sha1}
    )

    return s.dumps(kwargs)
