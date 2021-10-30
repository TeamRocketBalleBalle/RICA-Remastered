USE rica;
insert into users(UserID, userrole, Name, Email, Phone) values
("P-01","patient", "Roguedbear", "gonerogued@gmail.com", "1234567899"),
("P-02", "patient", "Codespicer", "codespicer@gmail.com", "9876543211"),
("D-01", "doctor", "S4DGE", "alwayssad@gmail.com", "9874563211"),
("D-02", "doctor", "Windy", "windy@gmail.com", "1236547891"),
("C-01", "chemist", "V4TSAL", "catsarecute@gmail.com", "8745316719"),
("C-02","chemist","aaaayuushhhh","valo@gmail.com","9475135687")
;


insert into patient(PatientID, Name) values
("P-01", "Roguedbear"),
("P-02", "Codespicer")
;

insert into doctor(DoctorID, Name, Degree, Bio, slot) values
("D-01", "Dr. S4DGE", "Nutritionist", "Gym jao", null),
("D-02", "Dr. Windy", "Eye surgeon", "aankh dikha", null)
;


insert into chemist(ChemistID, Name, location) values
("C-01", "V4TSAL", "Kullu Manali"),
("C-02", "aaaayuushhhh", "Indore")
;


insert into orders(PiD, CiD, prescription) values
("P-01", "C-01", JSON_Object("Vitamin C tablets", "5")),
("P-02", "C-02", JSON_Object("Patanjali Eye Drop", "100 ml"))
;


insert into appointments(BookingID, PiD, DiD, Timings) values
("B-01-nov03", "P-01", "D-01", "2021-11-03 11:30:00"),
("B-02-nov01", "P-02", "D-02", "2021-11-01 10:00:00")
;
