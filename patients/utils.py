import os
import threading
import time
from cryptography.fernet import Fernet

from patient_gateway.settings import get_secret


ENCRYPTION_KEY = get_secret('CRYPTOGRAPHY_KEY')

if not ENCRYPTION_KEY:
    raise RuntimeError("ENCRYPTION_KEY is not set")

fernet = Fernet(ENCRYPTION_KEY.encode())

# for encypting ssn and pssport number
def encrypt_value(value: str) -> str:
    if value is None:
        return None
    return fernet.encrypt(value.encode()).decode()

# for decrypting encrypted data
def decrypt_value(value: str) -> str:
    if value is None:
        return None
    return fernet.decrypt(value.encode()).decode()

def mask_values(value: dict) -> str:
    security_type = value['type']
    security_value = value['value']
    if not security_value:
        return None
    if security_type == 'ssn':
        digits = "".join(ch for ch in security_value if ch.isdigit())

        if len(digits) < 4:
            return "***"

        return "***-**-" + digits[-4:]
    
    if security_type == 'passport':
        visible = security_value[-4:]
        masked_length = max(len(security_value) - 4, 0)

        return "*" * masked_length + visible


def get_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")

def send_welcome_email(email, patient_name):
    #delay will be there in actual email sending
    time.sleep(2)
    print(f"Welcome email sent to {email} for patient {patient_name}")

def send_welcome_email_async(email, patient_name):
    thread = threading.Thread(
        target=send_welcome_email,
        args=(email, patient_name),
        daemon=True,
    )
    thread.start()