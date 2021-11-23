
insert into users(UserID, userrole, Name, Email, Location,Phone, pwhash) values
(1,"patient", "Roguedbear", "gonerogued@gmail.com", "Aligarh","1234567899", 'pbkdf2:sha256:260000$2lZe7hIHIKzN1XqW$2ef1d75eb5fb593b2eff8d76eaf0df216dea5c577b504a2696d25931f0cf59c9'),
(2, "patient", "Codespicer", "codespicer@gmail.com", "Greater Noida","9876543211", 'pbkdf2:sha256:260000$RtewttdNo2uNRXAq$a7a0855762706a2b41ac9c743dd5ed6e234179164b144613cdf03e86f0fa2ae4'),
(3, "doctor", "S4DGE", "alwayssad@gmail.com", "Greater Noida","9874563211", 'pbkdf2:sha256:260000$bKxq6JMF6n6HToed$5bf6d4fcc16a702fb58a36178d973375c86fa934977ffb1dad413e0bda495680'),
(4, "doctor", "Windy", "windy@gmail.com", "Rampur bushahar","1236547891", 'pbkdf2:sha256:260000$IQMgzbCsGzOzAGxe$5dc12fbed37c953db162f8320d73115ccdbb1f8741ddd0da2042147bbe9f8a06' ),
(5, "chemist", "V4TSAL", "catsarecute@gmail.com", "Kullu","8745316719", 'pbkdf2:sha256:260000$nyTCiRvZoiBOOFS7$81e431739eb40fd47dd8dd7a6d9e7fe92a0ba640e3107496b16d49550b1e1b6a'),
(6,"chemist","aaaayuushhhh","valo@gmail.com", "Indore","9475135687", 'pbkdf2:sha256:260000$ASszwxf0PLIdn397$2edff3bec5925d9604c7ebfd74ecc05699d8b0a0cf825217abde5db749ccde80'),
(7, "patient", "Lorem Ipsum", "LoremIpsum@lorem.ipsum", "New Jersey","9999999999", 'pbkdf2:sha256:260000$Ll0KCoYQb4hGZ5hn$b7613112bebdda364603cdffc06469fdd6fbd15644dd6474dae68f132cb0e72d')
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
(1, 5, JSON_Object("medicine_name", "Vitamin C tablets", "days","5", "Dose", "2")),
(2, 6, JSON_Object("medicine_name", "Patanjali Eye Drop", "days", "10", "dose", "3"))
;


insert into appointments(BookingID, PatientID, DoctorID, Timings, Confirmed) values
(1, 2, 3, "2021-11-03 11:30:00", true),
(2, 2, 4, "2021-11-01 10:00:00", false),
(3, 7, 4, "2021-11-05 05:30:00", false)
;
