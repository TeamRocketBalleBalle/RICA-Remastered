CREATE DATABASE IF NOT EXISTS rica;
USE rica;

CREATE TABLE IF NOT EXISTS users (
    UserID INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    userrole varchar(10) NOT NULL,
    Name varchar(30) NOT NULL,
    Email varchar(50) NOT NULL,
    Location varchar(30) NOT NULL,
    Phone varchar(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS patient (
    PatientID INTEGER NOT NULL,
    FOREIGN KEY (PatientID) REFERENCES users(UserID)
);

CREATE TABLE IF NOT EXISTS doctor(
    DoctorID INTEGER NOT NULL,
    Degree TEXT NOT NULL,
    Specialization varchar(30) NOT NULL,
    Bio TEXT ,
    slot JSON ,
    FOREIGN KEY (DoctorID) REFERENCES users(UserID)
);

CREATE TABLE IF NOT EXISTS chemist(
    ChemistID INTEGER NOT NULL,
    FOREIGN KEY (ChemistID) REFERENCES users(UserID)
);

CREATE TABLE IF NOT EXISTS orders(
    PatientID INTEGER NOT NULL,
    ChemistID INTEGER NOT NULL,
    prescription JSON NOT NULL,
    FOREIGN KEY (PatientID) REFERENCES patient(PatientID),
    FOREIGN KEY (ChemistID) REFERENCES chemist(ChemistID)
);

CREATE TABLE IF NOT EXISTS appointments(
    BookingID INTEGER NOT NULL,
    DoctorID INTEGER NOT NULL,
    PatientID INTEGER NOT NULL,
    Timings TIMESTAMP NOT NULL,
    Confirmed boolean NOT NULL,
    symptoms TEXT,
    FOREIGN KEY (PatientID) REFERENCES patient(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES doctor(DoctorID)
);

-- DELIMITER $$
--
-- CREATE TRIGGER after_patient_data_insert
-- AFTER INSERT
-- ON users FOR EACH ROW
-- BEGIN
--     IF NEW.userrole = 'patient' THEN
--         INSERT INTO patient(PatientID)
--         VALUE(NEW.UserID);
--     END IF;
-- END$$
--
-- DELIMITER ;
