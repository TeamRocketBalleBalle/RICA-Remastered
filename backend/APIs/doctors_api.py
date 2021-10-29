# Importing stiff required for this task...
import flask
from flask import current_app, request

from backend.utility.db_wrapper import get_cursor

bp = flask.Blueprint("doctors_api", __name__, url_prefix="/api/v1/doctors")


@bp.route('/appointment', methods=['GET'])
def get_list_of_bookings(DoctorId):
    """
    :param DoctorId:
    :return: JSON Object of the appointment for the respective DoctorId
    """
    cursor = current_app.mysql.connection.cursor()
    appointment = dict()
    DoctorId = request.args.get("doctorID")

    cursor.execute(
        f"SELECT BookingID FROM appointments WHERE DiD = {DoctorId}")
    for bookingId in cursor.fetchall():
        appointment["BookingID"] = bookingId

    cursor.execute(f"SELECT Timings FROM appointments WHERE DiD = {DoctorId}")
    for time in cursor.fetchall():
        appointment["Timing"] = time

    cursor.execute(
        f" select name from patient where PatientID in (SELECT PiD from appointments where DiD = {DoctorId})")
    for patientName in cursor.fetchall():
        appointment["PatientName"] = patientName

    cursor.close()
    return flask.jsonify(appointment)
