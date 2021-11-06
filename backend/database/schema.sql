CREATE DATABASE IF NOT EXISTS rica;
USE rica;
-- If, above syntax does not which will most likely be, just make a database in your sql server/ or whatever
-- MySQL client you are using

CREATE TABLE IF NOT EXISTS users (
    UserID varchar(5) NOT NULL PRIMARY KEY,
    userrole varchar(10) NOT NULL,
    Name varchar(30) NOT NULL,
    Email varchar(50) NOT NULL,
    Phone varchar(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS patient (
    PatientID varchar(10) NOT NULL,
    Name varchar(30) NOT NULL,
    FOREIGN KEY (PatientID) REFERENCES users(UserID)
);

CREATE TABLE IF NOT EXISTS doctor(
    DoctorID varchar(10) NOT NULL,
    Name varchar(30) NOT NULL,
    Degree TEXT NOT NULL,
    City varchar(30) NOT NULL,
    Specialization varchar(30) NOT NULL,
--    Bio JSON NOT NULL,
    Bio TEXT ,  -- No word Limit on TEXT datatype
    slot JSON ,
--    appointment JSON NOT NULL, -- No need of it
    FOREIGN KEY (DoctorID) REFERENCES users(UserID)
);

CREATE TABLE IF NOT EXISTS chemist(
    ChemistID varchar(10) NOT NULL,
    Name varchar(30) NOT NULL,
    location varchar(30) NOT NULL,
    FOREIGN KEY (ChemistID) REFERENCES users(UserID)
);

CREATE TABLE IF NOT EXISTS orders(
    PiD varchar(10) NOT NULL,
    CiD varchar(10) NOT NULL,
    prescription JSON NOT NULL,
    FOREIGN KEY (PiD) REFERENCES patient(PatientID),
    FOREIGN KEY (CiD) REFERENCES chemist(ChemistID)
);

CREATE TABLE IF NOT EXISTS appointments(
--    BookingID JSON NOT NULL, -- No need for it be in JSON
    BookingID varchar(10) NOT NULL,
    DiD varchar(10) NOT NULL,
    PiD varchar(10) NOT NULL,
    Timings TIMESTAMP NOT NULL,
    FOREIGN KEY (PiD) REFERENCES patient(PatientID),
    FOREIGN KEY (DiD) REFERENCES doctor(DoctorID)
);
