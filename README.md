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
git clone <private-repo-url>
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

# to run tests
python manage.py test patients.tests
