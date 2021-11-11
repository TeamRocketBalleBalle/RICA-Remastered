# Importing stiff required for this task...
import flask
from flask import jsonify, request, session

from backend.utility.db_wrapper import get_cursor

bp = flask.Blueprint("doctors_api", __name__, url_prefix="/api/v1/doctors")


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

    query = "SELECT name FROM users WHERE PatientID IN (SELECT PatientID FROM appointments WHERE BookingID = %s)"
    cursor.execute(query, (bookingId,))
    appointment["PatientName"] = cursor.fetchall()[0]

    cursor.close()
    return appointment


@bp.route('/appointment', methods=['GET'])
@get_cursor
def get_booking_info(cursor):
    user_id = session.get("id", "")

    # not possible since user input is never involved. aka set by the server, but still checking for "oddities
    if not isinstance(user_id, int):
        reason = {
            "status": "BAD REQUEST",
            "reason": f"\"{user_id}\" is not a valid user_id"
        }
        return jsonify(reason), 400

    query = " select userrole from users where UserID = %s"
    cursor.execute(query, (user_id,))
    userType = cursor.fetchone()
    # print(userType)
    temp = None

    # if somehow we have non-existent user id in the cookie
    if userType is None:
        reason = {"status": "BAD REQUEST",
                  "reason": f"\"{user_id}\" is not a valid user_id"
                  }
        return jsonify(reason), 400
    elif userType[0] == "doctor":
        temp = "DoctorID"   # about time DiD becomes DoctorID
    elif userType[0] == "patient":
        temp = "PatientID"  # about time PiD becomes PatientID
    elif userType[0] == "chemist":
        reason = {"status": "FORBIDDEN",
                  "reason": f"Chemists do not have appointments"
                  }
        return jsonify(reason), 403
    query = f"SELECT BookingID FROM appointments WHERE {temp} = %s"
    cursor.execute(query, (user_id,))
    id = cursor.fetchall()[0][0]
    return jsonify(detailed_appointment_info(id, cursor))
