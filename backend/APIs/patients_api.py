import flask
from flask import jsonify

from backend.APIs.doctors_api import get_booking_info
from backend.utility.db_wrapper import get_cursor

bp = flask.Blueprint("patients_api", __name__, url_prefix="/api/v1/patients")


def previous_appointment(Patientid):
    return get_booking_info(Patientid)


@get_cursor
def get_doc_names(city, specialization, cursor):
    query = "SELECT Name FROM doctor where City = %s AND Specialization = %s"
    cursor.execute(query, (city, specialization))
    return jsonify(cursor.fetchall())


@get_cursor
def search_doctors_using_name(Name: str, cursor):
    query = "SELECT Name from doctor where Name = %s"
    cursor.execute(query, (Name,))
    return jsonify(cursor.fetchall()[0])
