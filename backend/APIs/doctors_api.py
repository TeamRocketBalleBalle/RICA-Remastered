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
        reason = {"status": "BAD REQUEST",
                  "reason": f"\"{user_id}\" is not a valid user_id"
                  }
        return jsonify(reason), 400
    # for chemists, unauthorised for them since they dont have bookings
    elif userType[0] == "chemist":
        reason = {"status": "FORBIDDEN",
                  "reason": "Chemists do not have appointments"
                  }
        return jsonify(reason), 403

    # TODO: limit appointments by result

    response = {"appointments": []}

    query = "SELECT * FROM appointments WHERE %s IN (DoctorID, PatientID);"
    cursor.execute(query, (user_id, ))
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
