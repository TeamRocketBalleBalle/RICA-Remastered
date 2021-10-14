CREATE DATABASE IF NOT EXISTS rica;

CREATE TABLE IF NOT EXISTS user (
    UserID varchar(10) NOT NULL PRIMARY KEY,
    Name varchar(30) NOT NULL,
    Email varchar(50) NOT NULL,
    Phone int NOT NULL
);

CREATE TABLE IF NOT EXISTS patient (
    PatientID varchar(10) NOT NULL,
    Name varchar(30) NOT NULL,
    FOREIGN KEY (PatientID) REFERENCES user(UserID)
);

CREATE TABLE IF NOT EXISTS doctor(
    DoctorID varchar(10) NOT NULL,
    Name varchar(30) NOT NULL,
    Degree varchar(15) NOT NULL,
    Bio JSON NOT NULL,
    slot JSON NOT NULL,
    appointment JSON NOT NULL,
    FOREIGN KEY (DoctorID) REFERENCES user(UserID)
);

CREATE TABLE IF NOT EXISTS chemist(
    ChemistID varchar(10) NOT NULL,
    Name varchar(30) NOT NULL,
    location varchar(30) NOT NULL,
    FOREIGN KEY (ChemistID) REFERENCES user(UserID)
);

CREATE TABLE IF NOT EXISTS orders(
    PiD varchar(10) NOT NULL,
    CiD varchar(10) NOT NULL,
    prescription JSON NOT NULL,
    FOREIGN KEY (PiD) REFERENCES patient(PatientID),
    FOREIGN KEY (CiD) REFERENCES chemist(ChemistID)
);

CREATE TABLE IF NOT EXISTS appointments(
    BookingID JSON NOT NULL,
    DiD varchar(10) NOT NULL,
    PiD varchar(10) NOT NULL,
    Timings TIMESTAMP NOT NULL,
    FOREIGN KEY (PiD) REFERENCES patient(PatientID),
    FOREIGN KEY (PiD) REFERENCES doctor(DoctorID)
);