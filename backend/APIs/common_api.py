from datetime import timezone

import flask
from flask import jsonify, session

from backend.utility.db_wrapper import get_cursor

bp = flask.Blueprint("common_api", __name__, url_prefix="/api/v1/common")


@bp.route('/appointment', methods=['GET'])
@get_cursor
def get_booking_info(cursor):
    """
    :param ID of the user stored in cookie:
    :return JSON object containing [doctor_id, patient_id, time]:
    """
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
    response = {"appointments": []}
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
    elif userType[0] == "patient":
        query = "SELECT u.Name, u.Location, u.Phone, ap.timings FROM appointments ap, users u WHERE ap.DoctorID = u.UserID and ap.PatientID = %s;"
        cursor.execute(query, (user_id,))
        for row in cursor:
            appointment = {
                "doctor_name": row[0],
                "location": row[1],
                "phone_number": row[2],
                "time": row[3].astimezone(timezone.utc).isoformat()
            }
            response["appointments"].append(appointment)
    elif userType[0] == "doctor":
        query = "SELECT u.Name, u.Location, u.Phone, ap.timings FROM appointments ap, users u WHERE ap.PatientID = u.UserID and ap.DoctorID = %s;"
        cursor.execute(query, (user_id,))
        for row in cursor:
            appointment = {
                "patient_name": row[0],
                "location": row[1],
                "phone_number": row[2],
                "time": row[3].astimezone(timezone.utc).isoformat()
            }
            response["appointments"].append(appointment)
    # query = "SELECT * FROM appointments WHERE %s IN (DoctorID, PatientID);"
    # cursor.execute(query, (user_id,))
    # for row in cursor:
    #     appointment = {
    #         "doctor_id": row[1],
    #         "patient_id": row[2],
    #         # assuming db timestamp is in utc
    #         "time": row[3].astimezone(timezone.utc).isoformat()
    #     }
    #     # print(row[3].isoformat())
    #     response["appointments"].append(appointment)
    return jsonify(response), 200


@bp.route("/view_order_detail/")
@get_cursor
def view_order_details(cursor):
    """
    Function to get order details from database
    :param user_id from cookie:
    :return JSON object containing [user_name, location, phone_number, prescription]:
    """
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
    response = {"order_details": []}
    # If somehow we have non-existent user id in the cookie
    if userType is None:
        reason = {
            "status": "BAD REQUEST",
            "reason": f"\"{user_id}\" is not a valid user_id"
        }
        return jsonify(reason), 400

    elif userType[0] == "doctor":
        reason = {
            "status": "FORBIDDEN",
            "reason": "Doctors are not not allowed to see order details..."
        }
        return jsonify(reason), 403

    elif userType[0] == "chemist":
        query = "SELECT u.Name, u.Location, u.Phone, ord.prescription FROM orders ord, users u WHERE ord.PatientID = u.UserID and ord.ChemistID = %s;"
        cursor.execute(query, (user_id,))

        for row in cursor:
            order_detail = {
                "patient_name": row[0],
                "location": row[1],
                "phone_number": row[2],
                "prescription": row[3]
            }
            response["order_details"].append(order_detail)
    elif userType[0] == "patient":
        query = "SELECT u.Name, u.Location, u.Phone, ord.prescription FROM orders ord, users u WHERE ord.ChemistID = u.UserID and ord.PatientID = %s;"
        cursor.execute(query, (user_id,))

        for row in cursor:
            order_detail = {
                "chemist_name": row[0],
                "location": row[1],
                "phone_number": row[2],
                "prescription": row[3]
            }
            response["order_details"].append(order_detail)
    return jsonify(response), 200
