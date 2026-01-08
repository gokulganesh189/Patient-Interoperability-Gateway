from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from patients.models import PatientRecord, PatientCommunication


def valid_patient_payload():
    return {
        "resourceType": "Patient",
        "id": "example-1236",
        "gender": "male",
        "birthDate": "1990-01-01",
        "name": [
            {
                "use": "official",
                "family": "Chalmers",
                "given": ["Peter", "James"]
            }
        ],
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
                "value": "peter@example.com",
                "use": "work"
            }
        ]
    }


class PatientIntakeAPITest(APITestCase):

    def setUp(self):
        self.url = reverse("patient-intake")

    def test_patient_intake_success(self):
        response = self.client.post(
            self.url,
            valid_patient_payload(),
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PatientRecord.objects.count(), 1)
        self.assertEqual(PatientCommunication.objects.count(), 2)

    def test_patient_under_18_rejected(self):
        payload = valid_patient_payload()
        payload["birthDate"] = "2015-01-01"

        response = self.client.post(
            self.url,
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_417_EXPECTATION_FAILED)
        self.assertEqual(PatientRecord.objects.count(), 0)
