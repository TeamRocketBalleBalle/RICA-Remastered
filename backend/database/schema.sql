create database if not exists rica;

create TABLE IF NOT EXISTS user (
    UiD varchar(10) not null primary key,
    Name varchar(30) not null,
    Email varchar(50) not null,
    Phone int not null
    );

create TABLE IF NOT EXISTS patient (
    PiD varchar(10) not null,
    Name varchar(30) not null,
    FOREIGN KEY (PiD) REFERENCES user(UiD)
    );

create TABLE IF NOT EXISTS doctor(
    DiD varchar(10) not null,
    Name varchar(30) not null,
    Degree varchar(15) not null,
    FOREIGN KEY (DiD) REFERENCES user(UiD)
    );

create TABLE IF NOT EXISTS chemist(
    CiD varchar(10) not null,
    Name varchar(30) not null,
    location varchar(30) not null,
    FOREIGN KEY (CiD) REFERENCES user(UiD)
    );

create TABLE IF NOT EXISTS orders(
    PiD varchar(10) not null,
    CiD varchar(10) not null,
    prescription JSON not null,
    FOREIGN KEY (PiD) REFERENCES patient(PiD),
    FOREIGN KEY (CiD) REFERENCES chemist(CiD)
    );
