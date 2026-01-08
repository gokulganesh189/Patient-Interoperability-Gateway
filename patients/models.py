import uuid
from django.db import models
from django.conf import settings


class PatientRecord(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    fhir_patient_id = models.CharField(
        max_length=255,
        unique=True
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    gender = models.CharField(
        max_length=20
    )

    birth_date = models.DateField()

    # Encrypted column
    encrypted_ssn = models.TextField(
        null=True,
        blank=True
    )

    encrypted_passport_number = models.TextField(
        null=True,
        blank=True
    )

    raw_payload = models.JSONField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AccessLog(models.Model):
    """
    Audit log for patient data access.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    patient = models.ForeignKey(
        PatientRecord,
        on_delete=models.CASCADE,
        related_name="access_logs"
    )

    accessed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    ip_address = models.GenericIPAddressField()

    accessed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Access to {self.patient_id} at {self.accessed_at}"


class PatientCommunication(models.Model):
    """
    Stores patient phone/contact details.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    patient = models.ForeignKey(
        PatientRecord,
        on_delete=models.CASCADE,
        related_name="phones"
    )

    system = models.CharField(
        max_length=20
    )  # e.g., phone, email

    value = models.CharField(
        max_length=50
    )  

    use = models.CharField(
        max_length=20,
        null=True,
        blank=True
    ) 

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.system}: {self.value}"
