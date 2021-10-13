CREATE DATABASE IF NOT EXISTS rica;

CREATE TABLE IF NOT EXISTS user (
    UiD varchar(10) NOT NULL PRIMARY KEY,
    Name varchar(30) NOT NULL,
    Email varchar(50) NOT NULL,
    Phone int NOT NULL
);

CREATE TABLE IF NOT EXISTS patient (
    PiD varchar(10) NOT NULL,
    Name varchar(30) NOT NULL,
    FOREIGN KEY (PiD) REFERENCES user(UiD)
);

CREATE TABLE IF NOT EXISTS doctor(
    DiD varchar(10) NOT NULL,
    Name varchar(30) NOT NULL,
    Degree varchar(15) NOT NULL,
    FOREIGN KEY (DiD) REFERENCES user(UiD)
);

CREATE TABLE IF NOT EXISTS chemist(
    CiD varchar(10) NOT NULL,
    Name varchar(30) NOT NULL,
    location varchar(30) NOT NULL,
    FOREIGN KEY (CiD) REFERENCES user(UiD)
);

CREATE TABLE IF NOT EXISTS orders(
    PiD varchar(10) NOT NULL,
    CiD varchar(10) NOT NULL,
    prescription JSON NOT NULL,
    FOREIGN KEY (PiD) REFERENCES patient(PiD),
    FOREIGN KEY (CiD) REFERENCES chemist(CiD)
);
