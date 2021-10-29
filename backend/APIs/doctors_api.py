# Importing stuff required for this task...
import flask
from flask_mysqldb import MySQL

# Initializing app
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_DB"] = 'rica'
app.config['MYSQL_USER'] = 'root'
mysql = MySQL(app)

# Done to avoid MySQL.OperationalError(2006, '') and one more error too...(forget which one)
with app.app_context():
    conn = mysql.connect


def detailed_appointment_info(BookingId):
    """
    :param BookingId:
    :return: List of Booking ids
    """
    cursor = conn.cursor()
    appointment = dict()

    query = "SELECT DATE_FORMAT(Timings, '%%Y-%%m-%%dT%%TZ') FROM appointments WHERE BookingID = %s "
    cursor.execute(query, (BookingId,))
    appointment["Timing"] = cursor.fetchall()[0]

    query = "SELECT name FROM patient WHERE PatientID IN (SELECT PiD FROM appointments WHERE BookingID = %s)"
    cursor.execute(query, (BookingId,))
    appointment["PatientName"] = cursor.fetchall()[0]

    cursor.close()
    return appointment


def get_booking_info(ID):
    cursor = conn.cursor()
    query = " select userrole from users where UserID = %s"
    cursor.execute(query, (ID,))
    userType = cursor.fetchone()
    # print(userType)
    if userType[0] == "doctor":
        temp = "DiD"
    elif userType[0] == "patient":
        temp = "PiD"
    else:
        return None
    # print(temp)
    query = f"SELECT BookingID FROM appointments WHERE {temp} = %s"

    cursor.execute(query, (ID,))
    return cursor.fetchall()[0]


if __name__ == '__main__':
    BookingID = get_booking_info(1)
    print(detailed_appointment_info(BookingID))
