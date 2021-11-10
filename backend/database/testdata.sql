USE rica;
insert into users(UserID, userrole, Name, Email, Phone) values
("P01","patient", "Roguedbear", "gonerogued@gmail.com", "1234567899"),
("P02", "patient", "Codespicer", "codespicer@gmail.com", "9876543211"),
("D01", "doctor", "S4DGE", "alwayssad@gmail.com", "9874563211"),
("D02", "doctor", "Windy", "windy@gmail.com", "1236547891"),
("C01", "chemist", "V4TSAL", "catsarecute@gmail.com", "8745316719"),
("C02","chemist","aaaayuushhhh","valo@gmail.com","9475135687"),
("P03", "patient", "Lorem Ipsum", "LoremIpsum@lorem.ipsum", "9999999999")
;


insert into patient(PatientID, Name) values
("P01", "Roguedbear"),
("P02", "Codespicer"),
("P03", "Lorem Ipsum")
;

insert into doctor(DoctorID, Name, Specialization, City, Degree, Bio, slot) values
("D01", "Dr. S4DGE", "Nutritionist", "Noida", "MBBS", "Gym jao", null),
("D02", "Dr. Windy", "Eye surgeon", "Rampur bushahar", "MBBS", "aankh dikha", null)
;


insert into chemist(ChemistID, Name, location) values
("C01", "V4TSAL", "Kullu Manali"),
("C02", "aaaayuushhhh", "Indore")
;


insert into orders(PiD, CiD, prescription) values
("P01", "C01", JSON_Object("Vitamin C tablets", "5")),
("P02", "C02", JSON_Object("Patanjali Eye Drop", "100 ml"))
;


insert into appointments(BookingID, PiD, DiD, Timings) values
("B01nov03", "P01", "D01", "2021-11-03 11:30:00"),
("B02nov01", "P02", "D02", "2021-11-01 10:00:00"),
("B03nov05", "P01", "D02", "2021-11-05 05:30:00")
;
