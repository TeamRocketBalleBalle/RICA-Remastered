# RICA-Remastered

## Hello! 👋

The structure of how we'll work is what we did
[earlier](<(https://github.com/TeamRocketBalleBalle/Ricktionary)>). In separate
branches for individual pieces of work.

> **Note to Evaluator:** Our repository has more branches than `main` branch
> where code for those specific things is being developed. Those branches will
> have the latest commits than this `main` branch and you are encouraged to
> check those branches out too. \
> Once code has been developed for that particular category, it will be merged onto
> main.

## Setting up dev environment

1. install `pre-commit` \
   `pip install -r requirements-dev.txt`
2. Set up `pre-commit` as a "pre-commit hook" \
   `pre-commit install --install-hooks`

## Stuff to keep in mind:

-   Always pull before you start editing code
-   **DO NOT DIRECTLY COMMIT TO `main` BRANCH**
-   We'll be doing the development work on the `development` branch and `main`
    will be used to mark significant releases. \
     When your respective work is done, open a Pull Request from your branch to
    `development` branch.

    (Just like [last time](https://github.com/TeamRocketBalleBalle/Ricktionary))
    \

    ![wholesome](https://cdn.discordapp.com/attachments/794508344441700382/886658678437056522/wholesome_seal_of_approval.png)

## APIs List 👇

###**_For Patient_** (/api/v1/patients)

-   **get doctor details** (/get_doctors/) \

    -   _(To show the name of the available doctors)_
    -   No input required
    -   return `{"doctor_name", "doctor_id", "phone", "email", "location"}`

-   **book new appointment** (/new_appointment/) \
    -   Inputs:
        -   PatientID from session
        -   Form details("meeting-time", "symptoms", "doctor_id")
    -   return `{"status", "reason"}`
-   **order_medicine** (/order_medicine)\
    -   Inputs:
        -   PatientID from session
        -   Form details ('days', 'dosage', 'chemist_id')
    -   return `{'status', 'reason'}`
-   **view chemist** (/view_chemist) \
    -   Inputs:
        -   None
    -   return `{"chemist_name", "chemist_id", "phone", "email", "location"}`

### **_For Doctor_** (/api/v1/doctors)

-   **get new appointment details** (/new*appointment/) \
     *(To shows new appointments to doctor)\_

    -   Inputs:
        -   DoctorID from session
    -   return `{"status", "reason"}`

-   **confirm/delete appointment** (/confirm/delete*appointment/booking_id) \
     *(Updates the status of appointment to true or delete the appointment )\_

    -   Inputs:

        -   DoctorID from session
        -   BookingID from URL

    -   return `{"status", "reason"}`

### **_Common APIs_**(/api/v1/common)

-   **get booking info** (/appointment) \
    _(To show the details of all the appointment of a particular user)_ - Input:
    -UserID from session - If user is doctor - return `("patient_name", "location", "phone_number", "time")` -
    If user is Patient - return `("doctor_name", "location", "phone_number", "time")`
-   **view order details** (/view*order_details) \
    *(To show medicine order details)\_

    -   Input
        -   UserID from session
    -   If user is patient
        -   return
            `("chemist_name", "location", "phone_number", "prescription")`
    -   If user is chemist
        -   return
            `("patient_name", "location", "phone_number", "prescription")`

-   **Login**(/login)\

    -   Input:
        -   Form details('email', 'password')\
    -   return
        -   {'status', 'reason', 'usertype'}

-   **Register** (/register)
