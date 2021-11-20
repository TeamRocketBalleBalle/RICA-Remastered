from datetime import datetime

import flask
from flask import jsonify, request, session

from backend.utility.db_wrapper import get_cursor

bp = flask.Blueprint("patients_api", __name__, url_prefix="/api/v1/patients")


# # TODO: Check if the below URL is working or not
# @bp.route("/get_doc_names/<string:city>/<string:specialization>", methods=['GET'])
# @get_cursor
# def get_doc_names(city, specialization, cursor):
#     """
#     Search the doctor names using city and specialization as its input...
#     :param city:
#     :param specialization:
#     If successful
#         :return JSON object containing [doctor_id, doctor_name, phone_number]:
#     else
#         :return JSON object having [status, reason]:
#     """
#     if not isinstance(city, str):
#         reason = {
#             "status": "BAD REQUEST",
#             "reason": "Invalid city"
#         }
#         return jsonify(reason), 400
#     if not isinstance(specialization, str):
#         reason = {
#             "status": "BAD REQUEST",
#             "reason": "Invalid specialization"
#         }
#         return jsonify(reason), 400
#
#     query = "SELECT u.Name, u.UserID, u.Phone FROM users u, doctor d where u.Location = %s AND d.Specialization = %s"
#     cursor.execute(query, (city, specialization))
#     response = {'doctor_details': []}
#     for row in cursor:
#         doctor_detail = {
#             "doctor_id": row[1],
#             "doctor_name": row[0],
#             "phone_number": row[2]
#         }
#         response["doctor_details"].append(doctor_detail)
#     return jsonify(response), 200
#
#
# @bp.route("/search_doctor/<string:Name>", methods=['GET'])
# @get_cursor
# def search_doctors_using_name(Name, cursor):
#     """
#     Search doctor name using a sub-string of its Name
#     :param Name:
#     If successful
#         :return JSON object containing [doctor_id, doctor_name, phone_number]:
#     else
#         :return JSON object having [status, reason]:
#     """
#     if not isinstance(Name, str):
#         reason = {
#             "status": "BAD REQUEST",
#             "reason": "Invalid name"
#         }
#         return jsonify(reason), 400
#     # query = " SELECT u.Name, d.DoctorID from users u, doctor d where u.Name like %%s% and u.userrole = 'doctor' \
#               and u.UserID = d.DoctorID;"
#     # cursor.execute(query, (Name,))
#
#     # Don't use 👆 commented syntax because we need: like '%<char>'
#     # But we are receiving: %'<char>'%
#     # I was not able to find a better way than the following method 👇
#     # We are using like because if the input is `S` it can still give output as (S4DGE, 3)
#     cursor.execute(
#         "SELECT u.Name, d.DoctorID, u.Phone from users u, doctor d where u.Name like '%%s%' and u.userrole = 'doctor'"
#         " and u.UserID = d.DoctorID;",
#         Name)
#     response = {'doctor_details': []}
#
#     # We need doctor id because when add_new_appointment() function will be called then
#     # to store database we also need doctor id and I am hoping from Front End that they will
#     # give that function the doctor id
#     for row in cursor:
#         doctor_detail = {
#             "doctor_id": row[1],
#             "doctor_name": row[0],
#             "phone_Number": row[2]
#         }
#         response["doctor_details"].append(doctor_detail)
#     return jsonify(response), 200


@bp.route("/get_doctors/")
@get_cursor
def get_doctors(cursor):
    query = "SELECT u.Name, u.UserID, u.Phone, u.email,u.Location FROM users u, doctor d where d.DoctorID = u.UserID;"
    cursor.execute(query)
    response = {"doctor_details": []}
    for row in cursor:
        doctor_detail = {
            "doctor_name": row[0],
            "doctor_id": row[1],
            "phone": row[2],
            "email": row[3],
            "location": row[4]
        }
        response["doctor_details"].append(doctor_detail)
    return jsonify(response), 200


@bp.route('/new_appointment/', methods=['GET'])
@get_cursor
def add_new_appointment(cursor):
    patient_id = session.get("id", "")
    response = dict()
    status_code = 200
    if not isinstance(patient_id, int):
        response = {
            "status": "BAD REQUEST",
            "reason": f"\"{patient_id}\" is not a valid patient_id"
        }
        status_code = 400
        # return jsonify(response), 400
    query = " select userrole from users where UserID = %s"
    cursor.execute(query, (patient_id,))
    userType = cursor.fetchone()

    # if somehow we have non-existent user id in the cookie
    if userType is None:
        response = {
            "status": "BAD REQUEST",
            "reason": f"\"{patient_id}\" is not a valid patient_id"
        }
        status_code = 400
        # return jsonify(response), 400

    # Onlyy for patient
    elif userType[0] != "patient":
        response = {
            "status": "FORBIDDEN",
            "reason": f"{userType[0]} do not have access to book new appointments"
        }
        status_code = 403
        # return jsonify(response), 403
    else:
        if request.form:
            timing = request.form["meeting-time"]
            symptoms = request.form["symptoms"]
            # Subject to changes
            doctor_id = request.form["doctor_id"]
            timing = datetime.strptime(timing, "%Y-%m-%dT%H:%M").isoformat()
            query = "select DoctorID from doctor where UserID = %s;"
            cursor.execute(query, (doctor_id,))
            doc_existence = cursor.fetchone()
            if doc_existence is None:
                response = {
                    "status": "NOT FOUND",
                    "reason": "Doctor not recognised by server"
                }
                status_code = 404
            else:
                cursor.execute(
                    "SELECT BookingID FROM appointments ORDER BY BookingID DESC LIMIT 1;")
                booking_id = cursor.fetchone()[0] + 1
                query = """INSERT INTO appointments(BookingID, PatientID, DoctorID, Timings, Confirmed, symptoms)
                VALUES (%s, %s, %s, %s, %s, %s);"""

                cursor.execute(query, (booking_id, patient_id,
                               doctor_id, timing, 0, symptoms))
                response = {
                    "status": "OK",
                    "reason": "Appointment added"
                }
                status_code = 200
        else:
            response = {
                "status": "BAD REQUEST",
                "reason": "Not are the required fields are submitted"
            }
            status_code = 400
    return jsonify(response), status_code


@bp.route('/order_medicine')
@get_cursor
def order_medicine(cursor):
    patient_id = session.get("id", "")
    response = dict()
    status_code = 200
    if not isinstance(patient_id, int):
        response = {
            "status": "BAD REQUEST",
            "reason": f"\"{patient_id}\" is not a valid patient_id"
        }
        status_code = 400
        # return jsonify(response), 400
    query = " select userrole from users where UserID = %s"
    cursor.execute(query, (patient_id,))
    userType = cursor.fetchone()

    # if somehow we have non-existent user id in the cookie
    if userType is None:
        response = {
            "status": "BAD REQUEST",
            "reason": f"\"{patient_id}\" is not a valid patient_id"
        }
        status_code = 400
        # return jsonify(response), 400

    # Only for patient
    elif userType[0] != "patient":
        response = {
            "status": "FORBIDDEN",
            "reason": f"{userType[0]} do not have access to order medicine"
        }
        status_code = 403
        # return jsonify(response), 403
    else:
        if request.form:
            medicine_name = request.form['medicine_name']
            days = request.form['days']
            dose = request.form['dosage']
            chemist_id = request.form['chemist_id']

            query = "SELECT ChemistID from chemist where ChemistID = %s;"
            cursor.execute(query, (chemist_id,))
            chemist_exists = cursor.fetchone()

            if chemist_exists is None:
                response = {
                    "status": "NOT FOUND",
                    "reason": "Chemist not recognised by server"
                }
                status_code = 404
            else:
                query = """INSERT INTO orders(PatientID, ChemistID, prescription)
                VALUES(%s, %s, JSON_OBJECT('medicine_name', %s,'Dose', %s, 'Days', %s));"""

                cursor.execute(query, (patient_id, chemist_id,
                               medicine_name, dose, days))
                response = {
                    "status": "OK",
                    "reason": "Medicine ordered successfully"
                }
                status_code = 200
    return jsonify(response), status_code


@bp.route('view_chemist')
@get_cursor
def view_chemist():
    query = "SELECT u.Name, u.UserID, u.Phone, u.email,u.Location FROM users u, chemist c where c.ChemistID = u.UserID;"
    cursor.execute(query)
    response = {"chemist_details": []}
    for row in cursor:
        chemist_detail = {
            "chemist_name": row[0],
            "chemist_id": row[1],
            "phone": row[2],
            "email": row[3],
            "location": row[4]
        }
        response["chemist_details"].append(chemist_detail)
    return jsonify(response), 200
