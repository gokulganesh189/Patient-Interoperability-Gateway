from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from patients.models import PatientRecord, PatientCommunication, AccessLog
from patients.utils import encrypt_value


class PatientDetailAPITest(APITestCase):

    def setUp(self):
        # User for JWT
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        # Patient record
        self.patient = PatientRecord.objects.create(
            fhir_patient_id="example-1237",
            first_name="Peter",
            last_name="Chalmers",
            gender="male",
            birth_date="1990-01-01",
            encrypted_ssn=encrypt_value("000-12-3456"),
            encrypted_passport_number=encrypt_value("M12345678"),
            raw_payload={"resourceType": "Patient"}
        )

        # Communications
        PatientCommunication.objects.bulk_create([
            PatientCommunication(
                patient=self.patient,
                system="phone",
                value="(555) 555-5555",
                use="home"
            ),
            PatientCommunication(
                patient=self.patient,
                system="phone",
                value="(555) 111-2222",
                use="mobile"
            )
        ])

        self.token_url = reverse("token_obtain_pair")
        self.detail_url = reverse(
            "patient-detail",
            kwargs={"patient_id": self.patient.id}
        )

    def authenticate(self):
        response = self.client.post(
            self.token_url,
            {
                "username": "testuser",
                "password": "testpassword"
            },
            format="json"
        )
        token = response.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )

    def test_patient_detail_authenticated(self):
        self.authenticate()

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data["data"]

        self.assertEqual(data["first_name"], "Peter")
        self.assertEqual(data["last_name"], "Chalmers")
        self.assertEqual(data["ssn"], "***-**-3456")
        self.assertEqual(len(data["phones"]), 2)

        # Audit log created
        self.assertEqual(AccessLog.objects.count(), 1)

    def test_patient_detail_unauthorized(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
