# Patient-Interoperability-Gateway
This application stores patient details and retrive them as pwe user requirements

## Tech Stack

- Python 3.10+
- Django
- Django REST Framework (DRF)
- Simple JWT (Authentication)
- PostgreSQL / SQLite (for local testing)
- cryptography (Fernet encryption)

## Setup Instructions
python3 -m venv env
cd env
pip install --upgrade pip
pip install -r requirements.txt
unzip the secrets file attached in the repo



### Clone Repository / Unzip Project

```bash
git clone https://github.com/gokulganesh189/Patient-Interoperability-Gateway.git
cd patient_gateway
```
# commands to setup server
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver


# api to get token
POST /api/v1/token/
{
  "username": "your_username",
  "password": "your_password"
}
Authorization: Bearer <access_token>

# api endpoints
| Method | Endpoint                   | Description                          |
| ------ | -------------------------- | ------------------------------------ |
| POST   | `/api/v1/patient-intake/`  | Ingest patient data                  |
| GET    | `/api/v1/patients/<uuid>/` | Fetch patient details (JWT required) |
| POST   | `/api/v1/token/`           | Obtain JWT token                     |
| POST   | `/api/v1/token/refresh/`   | Refresh JWT token                    |

# url, payload and response
==========================
1 get token
url: http://127.0.0.1:8000/api/v1/token/
method: POST
payload: {
  "username": "user_name",
  "password": "password"
}
response: {"refresh":"refresh token","access":"access token"}
===========================

==========================
2 Load Patient
url: http://127.0.0.1:8000/api/v1/patient-intake/
method: POST
payload: {
"resourceType": "Patient",
"id": "example-14367",
"active": true,
"name": [
{
"use": "official",
"family": "Chalmers",
"given": ["Peter", "James"]
}
],
"gender": "male",
"birthDate": "1980-12-25",
"identifier": [
{
"system": "http://hl7.org/fhir/sid/us-ssn",
"value": "000-12-3456"
}
],
"telecom": [
{
"system": "phone",
"value": "(555) 555-5555",
"use": "home"
},
{
"system": "email",
"value": "testuser189@gmail.com",
"use": "home"
}
]
}
response: {"message":"Patient record created","status":"Sucess"}
===========================

==========================
3 get user details
url: http://127.0.0.1:8000/api/v1/patients/<patient_id>/
method: GET
response: {"message":"Patient details retrieved","data":{"id":"aa66eef2-e4bb-4a9c-a19c-30fec0ce2ef1","first_name":"Peter","last_name":"Chalmers","gender":"male","birth_date":"1980-12-25","ssn":"***-**-3456","passport":null,"phones":[{"type":"home","number":"(555) 555-5555"}]}}
note: Need JWT token to access this api (authenticatedused only)
===========================


# to run tests
python manage.py test patients.tests

# Design Deicision
I have used Fernet in the cryptograpthy module to encrypt SSN and possible passport number. To create ENCRYPTION_KEY use command all logic to encrpt and decrypt is included in the patient/utils.y file
```
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

# TODO
If I got some more time I would have make a docker file and contanerized the application.
