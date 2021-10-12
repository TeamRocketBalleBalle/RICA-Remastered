import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
)

cursor = conn.cursor()

"""
    Dropping the if it exists
    Then creating a fresh new Database
    (I think this is Dynamic)

"""

cursor.execute("drop database if exists rica")
cursor.execute("create database rica")

# Creating tables (User, Patient, Doctor, Chemist, Biometric, Order, History)

# Making **user** table
cursor.execute("""Create table user(
UiD varchar(10) not null primary key,
Name varchar(30) not null,
Email varchar(50) not null,
Phone int not null
)""")

# Making **patient** table
cursor.execute("""create table patient(
PiD varchar(10) not null,
Name varchar(30), not null,
FOREIGN KEY (PiD) REFERENCES user(UiD)
)""")

# Making **doctor** table
cursor.execute("""create table doctor(
DiD int not null,
Name varchar(30) not null,
Degree varchar(15) not null,
FOREIGN KEY (DiD) REFERENCES user(UiD)
)""")

# Making **chemist** table
cursor.execute("""create table chemist(
CiD int not null,
Name varchar(30) not null,
location varchar(30) not null,
FOREIGN KEY (CiD) REFERENCES user(UiD)
)""")

# Making **history** table
cursor.execute("""create table chemist(
PiD int not null,
DiD int not null,
prescription JSON not null,
FOREIGN KEY (PiD) REFERENCES patient(PiD),
FOREIGN KEY (DiD) REFERENCES doctor(DiD),
)""")

# Making **order** table
cursor.execute("""create table chemist(
PiD int not null,
CiD int not null,
prescription JSON not null,
FOREIGN KEY (PiD) REFERENCES patient(PiD),
FOREIGN KEY (CiD) REFERENCES chemist(CiD),
)""")

conn.commit()

print(cursor.rowcount, "record inserted.")
conn.close()
