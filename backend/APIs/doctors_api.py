# Importing stiff required for this task...
import flask
from flask_mysqldb import MySQL

# Initializing app
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["MYSQL_DB"] = 'rica'
app.config['MYSQL_USER'] = 'root'
mysql = MySQL(app)

# Done to avoid MySQL.OperationalError(2006, '') and one more error too...(forget which one)
with app.app_context():
    conn = mysql.connect


@app.route('/doctor/appointment', methods=['GET'])
def get_list_of_bookings(DoctorId):
    """
    :param DoctorId:
    :return: JSON Object of the appointment for the respective DoctorId
    """
    cursor = conn.cursor()
    appointment = dict()

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


if __name__ == '__main__':
    app.run()
