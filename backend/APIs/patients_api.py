import flask
from flask import jsonify, session

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
#     # query = " SELECT u.Name, d.DoctorID from users u, doctor d where u.Name like %%s% and u.userrole = 'doctor' and u.UserID = d.DoctorID;"
#     # cursor.execute(query, (Name,))
#
#     # Don't use 👆 commented syntax because we need: like '%<char>'
#     # But we are receiving: %'<char>'%
#     # I was not able to find a better way than the following method 👇
#     # We are using like because if the input is `S` it can still give output as (S4DGE, 3)
#     cursor.execute(
#         "SELECT u.Name, d.DoctorID, u.Phone from users u, doctor d where u.Name like '%%s%' and u.userrole = 'doctor' and u.UserID = d.DoctorID;",
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
def add_new_appointment(doctor_id, cursor):
    patient_id = session.get("id", "")
    # TODO: Ponder the question how will it receive time and Symptoms? Will it be a JSON?
