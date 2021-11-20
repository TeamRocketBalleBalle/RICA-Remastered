import re
from datetime import timezone

import flask
from flask import jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash

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
        query = "SELECT u.Name, u.Location, u.Phone, ap.timings FROM appointments ap, users u WHERE ap.DoctorID = " \
                "u.UserID and ap.PatientID = %s;"
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
        query = "SELECT u.Name, u.Location, u.Phone, ap.timings FROM appointments ap, users u WHERE ap.PatientID = " \
                "u.UserID and ap.DoctorID = %s;"
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
        query = "SELECT u.Name, u.Location, u.Phone, ord.prescription FROM orders ord, users u WHERE ord.PatientID = " \
                "u.UserID and ord.ChemistID = %s;"
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
        query = "SELECT u.Name, u.Location, u.Phone, ord.prescription FROM orders ord, users u WHERE ord.ChemistID = "\
                "u.UserID and ord.PatientID = %s;"
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


@bp.route("/login", methods=['GET', "POST"])
@get_cursor
def login(cursor):
    """

    - If 'id' is not in the session dictionary, then user is not logged in.
        - Then login the user store their email in the session cookie
    - If 'id' is in the sessions dictionary, and we're on login page:
        - Log them out, clear the sessions dictionary

    """
    response = dict()
    status_code = 200
    if request.form and 'id' not in session:
        email = request.form['email']
        password = request.form['password']

        query = "SELECT Email from users where Email = %s;"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        query = "SELECT userrole from users where Email = %s;"
        cursor.execute(query, (email,))
        usertype = cursor.fetchone()[0]
        # If email does not exists in database
        if user is None:
            response = {
                "status": "NOT FOUND",
                "reason": f"No account matches with this {email}"
            }
            # return jsonify(response), 404
            status_code = 404

        # Email exists
        else:
            query = "SELECT pwhash FROM users where Email = %s;"
            cursor.execute(query, (email,))
            hashed_password = cursor.fetchone()[0]

            # Email exists in database and password is correct
            if (check_password_hash(hashed_password, password)):
                query = "SELECT UserID FROM users where Email = %s;"
                cursor.execute(query, (email,))
                session['id'] = cursor.fetchone()
                response = {
                    "status": "OK",
                    "reason": "Login Successful",
                    "usertype": usertype
                }
                status_code = 200
                # return jsonify(response), 200
            # Email exists in database but password is wrong
            else:
                response = {
                    "status": "Unauthorized",
                    "reason": "Wrong password"
                }
                # return jsonify(response), 401
                status_code = 401

    # User is already logged-in
    elif 'id' in session:
        session.clear()
        response = {
            "status": "Continue",
            "reason": "You have been successfully logout... Try login again"
        }
        # return jsonify(response), 100
        status_code = 100

    # Form is empty
    else:
        response = {
            "status": "BAD REQUEST",
            "reason": "Enter username/password"
        }
        status_code = 400
        # return jsonify(response), 400
    return jsonify(response), status_code


@bp.route('/register')
@get_cursor
def register(cursor):
    response = dict()
    status_code = 200
    # Form not empty aka no blank inputs
    if request.form:
        name = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        phone = request.form['number']
        location = request.form['address']
        userrole = request.form['usertype']

        query = "SELECT Email FROM users where email = %s;"
        cursor.execute(query, (email))
        existence = cursor.fetchone()
        EMAIL_REGEX = re.compile(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+")

        # Email is valid -> has "@" and "."
        if EMAIL_REGEX.match(email):
            # Email exists in Database
            if existence is not None:
                response = {
                    "status": "CONFLICT",
                    "reason": f"Account already exist with {email}"
                }
                status_code = 409
                # return jsonify(response), 409
            # New user/email
            else:

                # If user is patient/chemist and has entered degree or specialization
                if userrole != 'doctor':
                    try:
                        degree = request.form['degree']
                        specialization = request.form['specialisation']
                    except Exception:
                        pass
                    else:
                        response = {
                            "status": "BAD REQUEST",
                            "reason": "Degree and Specialisation are only limited to doctor"
                        }
                        status_code = 400
                        # return jsonify(response), 400
                # if user is doctor and has not entered degree or specialization
                else:
                    try:
                        degree = request.form['degree']
                        specialization = request.form['specialisation']
                    except Exception:
                        response = {
                            "status": "BAD REQUEST",
                            "reason": "Enter degree/specialization"
                        }
                        status_code = 400
                        # return jsonify(response), 400
                    else:
                        pass

                query = "INSERT INTO users(userrole, Name, Email, Location, phone, pwhash)" \
                        " VALUES(%s, %s, %s, %s, %s, %s);"
                values = (userrole, name, email, location, phone, password)
                cursor.execute(query, values)
                cursor.commit()
                if userrole != 'doctor':
                    query = "SELECT UserID from users where email =  %s;"
                    cursor.execute(query, (email,))
                    user_id = cursor.fetchone()[0]
                    query = "INSERT INTO %s values(%s);"
                    cursor.execute(query, (userrole, user_id))
                    cursor.commit()
                else:
                    query = "SELECT UserID from users where email =  %s;"
                    cursor.execute(query, (email,))
                    user_id = cursor.fetchone()[0]

                    query = "INSERT INTO doctor values(%s, %s, %s);"
                    cursor.execute(query, (user_id, degree, specialization))
                    cursor.commit()
        else:
            response = {
                "status": "BAD REQUEST",
                "reason": "Not a valid email"
            }
            status_code = 400
    else:
        response = {
            "status": "BAD REQUEST",
            "reason": "It seemed you missed something in the form... Try again"
        }
        status_code = 400

    return jsonify(response), status_code
