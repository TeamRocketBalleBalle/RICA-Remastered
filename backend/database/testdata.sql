USE rica;
insert into users(UserID, userrole, Name, Email, Location,Phone) values
(1,"patient", "Roguedbear", "gonerogued@gmail.com", "No Wi-Fi Zone","1234567899"),
(2, "patient", "Codespicer", "codespicer@gmail.com", "Jeb mein","9876543211"),
(3, "doctor", "S4DGE", "alwayssad@gmail.com", "Himanshu ke ghar pr","9874563211"),
(4, "doctor", "Windy", "windy@gmail.com", "Rampur bushahar","1236547891"),
(5, "chemist", "V4TSAL", "catsarecute@gmail.com", "Kullu mein kahi pr","8745316719"),
(6,"chemist","aaaayuushhhh","valo@gmail.com", "Indore","9475135687"),
(7, "patient", "Lorem Ipsum", "LoremIpsum@lorem.ipsum", "Idk","9999999999")
;


insert into patient(PatientID) values
(1),
(2),
(7)
;

insert into doctor(DoctorID, Specialization, Degree, Bio, slot) values
(3, "Nutritionist", "MBBS", "Gym jao", null),
(4, "Eye surgeon", "MBBS", "aankh dikha", null)
;


insert into chemist(ChemistID) values
(5),
(6)
;


insert into orders(PatientID, ChemistID, prescription) values
(1, 5, JSON_Object("Vitamin C tablets", "5")),
(2, 6, JSON_Object("Patanjali Eye Drop", "100 ml"))
;


insert into appointments(BookingID, PatientID, DoctorID, Timings) values
("B01nov03", 1, 3, "2021-11-03 11:30:00"),
("B02nov01", 1, 4, "2021-11-01 10:00:00"),
("B03nov05", 1, 4, "2021-11-05 05:30:00")
;
