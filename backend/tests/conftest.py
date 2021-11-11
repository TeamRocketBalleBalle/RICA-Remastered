import pytest
from flask import current_app

from backend import create_app
from backend.database.db_cli import addData, delete_db, makeDb

SECRET_KEY = "testing"


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    app.secret_key = SECRET_KEY

    with app.test_client() as client:
        # setup db
        with app.app_context():
            conn = current_app.mysql.connection
            cursor = conn.cursor()

            delete_db(cursor)
            makeDb(cursor)
            addData(cursor)

            cursor.close()
            conn.commit()

        yield client

        # teardown db
        with app.app_context():
            conn = current_app.mysql.connection
            cursor = conn.cursor()

            delete_db(cursor)

            cursor.close()
            conn.commit()
