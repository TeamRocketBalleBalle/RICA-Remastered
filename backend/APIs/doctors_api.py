# Importing stiff required for this task...
from datetime import timezone

import flask
from flask import jsonify, session

from backend.utility.db_wrapper import get_cursor

bp = flask.Blueprint("doctors_api", __name__, url_prefix="/api/v1/doctors")


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

    # if somehow we have non-existent user id in the cookie
    if userType is None:
        reason = {
            "status": "BAD REQUEST",
            "reason": f"\"{user_id}\" is not a valid user_id"
        }
        return jsonify(reason), 400
    # for chemists, unauthorised for them since they dont have bookings
    elif userType[0] == "chemist":
        reason = {
            "status": "FORBIDDEN",
            "reason": "Chemists do not have appointments"
        }
        return jsonify(reason), 403

    # TODO: limit appointments by result

    response = {"appointments": []}

    query = "SELECT * FROM appointments WHERE %s IN (DoctorID, PatientID) and Confirmed = true;"
    cursor.execute(query, (user_id,))
    for row in cursor:
        appointment = {
            "doctor_id": row[1],
            "patient_id": row[2],
            # assuming db timestamp is in utc
            "time": row[3].astimezone(timezone.utc).isoformat()
        }
        # print(row[3].isoformat())
        response["appointments"].append(appointment)

    return jsonify(response), 200


@bp.route("/new_appointment/", methods=['GET'])
@get_cursor
def get_new_appointment_details(cursor):
    doctor_id = session.get("id", "")
    # not possible since user input is never involved. aka set by the server, but still checking for "oddities
    if not isinstance(doctor_id, int):
        reason = {
            "status": "BAD REQUEST",
            "reason": f"\"{doctor_id}\" is not a valid doctor_id"
        }
        return jsonify(reason), 400

    query = " select userrole from users where UserID = %s"
    cursor.execute(query, (doctor_id,))
    userType = cursor.fetchone()

    # if somehow we have non-existent user id in the cookie
    if userType is None:
        reason = {
            "status": "BAD REQUEST",
            "reason": f"\"{doctor_id}\" is not a valid doctor_id"
        }
        return jsonify(reason), 400

    # for chemists, unauthorised for them since they dont have bookings
    elif userType[0] == "chemist":
        reason = {
            "status": "FORBIDDEN",
            "reason": "Chemists do not have appointments"
        }
        return jsonify(reason), 403

    query = "SELECT a.BookingID, a.Timings, u.Name FROM appointments a, users u where Confirmed = false and DoctorID = %s and u.UserID = a.PatientID;"
    cursor.execute(query, (doctor_id,))
    response = {'booking_info': []}
    for row in cursor:
        booking_details = {
            'booking_id': row[0],
            'timings': row[1],
            'patient_name': row[2]
        }
        response['booking_info'].append(booking_details)
    return jsonify(response), 200


# TODO: How to send confirmation to patient about their appointment status? And Should we send them?
@bp.route("/confirm_appointment/<int:booking_id>")
@get_cursor
def confirm_appointment(booking_id, cursor):
    doctor_id = session.get("id", "")

    if not isinstance(doctor_id, int):
        reason = {
            "status": "BAD REQUEST",
            "reason": f"{doctor_id} is not a valid doctor ID "
        }
        return jsonify(reason), 400

    if not isinstance(booking_id, int):
        reason = {
            "status": "BAD REQUEST",
            "reason": f"{booking_id} is not a valid booking ID "
        }
        return jsonify(reason), 400

    query = " select userrole from users where UserID = %s"
    cursor.execute(query, (doctor_id,))
    userType = cursor.fetchone()

    # if somehow we have non-existent user id in the cookie
    if userType is None:
        reason = {
            "status": "BAD REQUEST",
            "reason": f"\"{doctor_id}\" is not a valid doctor_id"
        }
        return jsonify(reason), 400

    # for chemists, unauthorised for them since they dont have bookings
    elif userType[0] == "chemist":
        reason = {
            "status": "FORBIDDEN",
            "reason": "Chemists do not have appointments"
        }
        return jsonify(reason), 403

    query = " select BookingID from appointments where BookingID = %s"
    cursor.execute(query, (booking_id,))
    id = cursor.fetchone()

    if id is None:
        reason = {
            "status": "BAD REQUEST",
            "reason": f"No record of given {booking_id} exists"
        }
        return jsonify(reason), 400

    query = "update appointments set Confirmed = true where BookingID = %s"
    cursor.execute(query, (booking_id,))
    response = {"response": "Appointment confirmed!"}
    return jsonify(response), 200


@bp.route("/delete_appointment/<int:booking_id>")
@get_cursor
def delete_appointment(booking_id, cursor):
    doctor_id = session.get("id", "")

    if not isinstance(doctor_id, int):
        reason = {
            "status": "BAD REQUEST",
            "reason": f"{doctor_id} is not a valid doctor ID "
        }
        return jsonify(reason), 400

    if not isinstance(booking_id, int):
        reason = {
            "status": "BAD REQUEST",
            "reason": f"{booking_id} is not a valid booking ID "
        }
        return jsonify(reason), 400

    query = " select userrole from users where UserID = %s"
    cursor.execute(query, (doctor_id,))
    userType = cursor.fetchone()

    # if somehow we have non-existent user id in the cookie
    if userType is None:
        reason = {
            "status": "BAD REQUEST",
            "reason": f"\"{doctor_id}\" is not a valid doctor_id"
        }
        return jsonify(reason), 400

    # for chemists, unauthorised for them since they dont have bookings
    elif userType[0] == "chemist":
        reason = {
            "status": "FORBIDDEN",
            "reason": "Chemists do not have appointments"
        }
        return jsonify(reason), 403

    query = " select BookingID from appointments where BookingID = %s and Confirmed = false;"
    cursor.execute(query, (booking_id,))
    id = cursor.fetchone()

    if id is None:
        reason = {
            "status": "BAD REQUEST",
            "reason": f"No record of given {booking_id} exists"
        }
        return jsonify(reason), 400

    query = "delete from appointments where BookingID = %s"
    cursor.execute(query, (booking_id,))
    response = {"response": "Appointment declined!"}
    return jsonify(response), 200
