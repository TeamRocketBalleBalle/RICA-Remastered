# Importing stiff required for this task...
import flask
from flask import jsonify, request, session

from backend.utility.db_wrapper import get_cursor

bp = flask.Blueprint("doctors_api", __name__, url_prefix="/api/v1/doctors")


@get_cursor
def detailed_appointment_info(bookingId, cursor):
    """
    :param bookingId:
    :param cursor:
    :return: List of Booking ids
    """
    appointment = dict()

    query = "SELECT DATE_FORMAT(Timings, '%%Y-%%m-%%dT%%TZ') FROM appointments WHERE BookingID = %s "
    cursor.execute(query, (bookingId,))
    appointment["Timing"] = cursor.fetchall()[0]

    query = "SELECT name FROM patient WHERE PatientID IN (SELECT PiD FROM appointments WHERE BookingID = %s)"
    cursor.execute(query, (bookingId,))
    appointment["PatientName"] = cursor.fetchall()[0]

    cursor.close()
    return appointment


@bp.route('/appointment', methods=['GET'])
@get_cursor
def get_booking_info(cursor):
    try:
        ID = session['user_id']
        if type(ID) == str:
            raise "id is string"
        elif type(ID) == float:
            raise 401
        elif ID is None:
            raise (401, "/appointment endpoint does not exist")
        query = " select userrole from users where UserID = %s"
        cursor.execute(query, (ID,))
        userType = cursor.fetchone()
        # print(userType)
        temp = None

        if userType[0] == "doctor":
            temp = "DiD"
        elif userType[0] == "patient":
            temp = "PiD"
        elif userType[0] == "chemist":
            raise 403
        query = f"SELECT BookingID FROM appointments WHERE {temp} = %s"
        cursor.execute(query, (ID,))
        id = cursor.fetchall()[0]
        return jsonify(detailed_appointment_info(id))
    except Exception as e:
        return "", e
