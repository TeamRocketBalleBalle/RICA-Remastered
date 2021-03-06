import logging
import os

from colorama import Fore, init
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from flask_mysqldb import MySQL

load_dotenv()


def config_app(app: Flask):
    app.config["MYSQL_DB"] = os.getenv("RICA_MYSQL_DB", 'rica')
    app.config["MYSQL_HOST"] = os.getenv("RICA_MYSQL_HOST", "localhost")
    app.config['MYSQL_USER'] = os.getenv("RICA_MYSQL_USER", 'root')
    app.config["MYSQL_PASSWORD"] = os.getenv("RICA_MYSQL_PASSWORD", "")
    app.config["MYSQL_DB"] = os.getenv("RICA_MYSQL_DB", "rica")

    # no default value because you need to provide a secret key if FLASK_ENV is not development
    app.config["SECRET_KEY"] = 'dev' if os.getenv(
        "FLASK_ENV", "development") == "development" else os.getenv("RICA_SECRET_KEY")

    app.mysql = MySQL(app)
    CORS(app, withCredentials=True, supports_credentials=True)
    setup_logger(app)


# ================================================================
# initialise Colorama
init(autoreset=True)


# Creating the logger filter class
# TODO: do something about logging
class IPFilter(logging.Filter):
    def filter(self, record):
        # TODO: replace this with user's email
        # try:
        #     email = session['username']
        # except KeyError as e:
        #     print(Fore.RED + "this happened:", e)
        #     email = ""
        record.ip_address = Fore.LIGHTBLUE_EX + request.remote_addr
        return True


def setup_logger(app: Flask):
    # Configure logging for app.logger
    # TODO: fix this
    # app.logger.handlers[0].setFormatter(
    #     logging.Formatter("%(ip_address)s - [%(asctime)s] %(levelname)-6s [%(module)s.py -> %(funcName)s()]: "
    #                       "\"%(message)s\"",
    #                       datefmt="%d/%b/%Y %H:%M:%S"
    #                       )
    # )
    # app.logger.setLevel(20)  # set logger to debug
    # app.logger.addFilter(IPFilter())
    pass


# ==============================================================

def create_app():
    """
    creates the flask app object.
    """
    # create and configure the app
    app = Flask(__name__)
    register_cli_commands(app)
    register_blueprints(app)
    config_app(app)

    return app


def register_blueprints(app: Flask):
    from backend.APIs import common, common_api, doctors_api, patients_api

    app.register_blueprint(doctors_api.bp)
    app.register_blueprint(patients_api.bp)
    app.register_blueprint(common.bp)
    app.register_blueprint(common_api.bp)


def register_cli_commands(app: Flask):
    from backend.database.db_cli import delete_db_command, init_db_command, testdata_db_command
    app.cli.add_command(init_db_command)
    app.cli.add_command(testdata_db_command)
    app.cli.add_command(delete_db_command)


if __name__ == '__main__':
    app = create_app()
    app.run()
