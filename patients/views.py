import traceback
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db import transaction


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from .models import PatientRecord, AccessLog, PatientCommunication
from .serializers import PatientIntakeSerializer
from .utils import encrypt_value, decrypt_value, mask_values, get_ip, send_welcome_email_async
# from django.db import transaction


class PatientIntakeView(APIView):

    def post(self, request):
        
        try:
            serializer = PatientIntakeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            data = serializer.validated_data
            encrypted_ssn = encrypt_value(data.get("ssn")) if data.get("ssn") else None
            encrypted_passport  = encrypt_value(data.get("passport")) if data.get("passport") else None

            payload = request.data
            official_name = None
            for name in payload.get("name", []):
                if name.get("use") == "official":
                    official_name = name
                    break

            if not official_name and payload.get("name"):
                official_name = data["name"][0]

            first_name = official_name.get("given", [None])[0]
            last_name = official_name.get("family")

            patient = PatientRecord.objects.create(
                fhir_patient_id=payload.get("id"),
                first_name=first_name,
                last_name=last_name,
                gender=payload.get("gender"),
                birth_date=data.get("parsed_birth_date"),
                encrypted_ssn=encrypted_ssn,
                encrypted_passport_number=encrypted_passport,
                raw_payload=payload,   
            )

            #save_phone details
            phone_objects = []
            email = None

            for telecom in payload.get("telecom", []):
                if telecom.get("system") is not None:
                    phone_objects.append(
                        PatientCommunication(
                            patient=patient,
                            system=telecom.get("system"),
                            value=telecom.get("value"),
                            use=telecom.get("use"),
                        )
                    )
                    if telecom.get("system") == "email" and email is None:
                        email = telecom.get("value")

            if phone_objects:
                PatientCommunication.objects.bulk_create(phone_objects)

            # email sending part just simulation
            if email:
                transaction.on_commit(
                    lambda: send_welcome_email_async(
                        email, f"{first_name} {last_name}"
                    )
                )

            return Response(
                {"message": "Patient record created", "status":"Sucess"},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"message": str(e), "status":"Error", "traceback":str(traceback.format_exc())},
                status=status.HTTP_417_EXPECTATION_FAILED
            )


class PatientDetailView(APIView):
    permission_classes = [IsAuthenticated]
    """
    1. Api fetch patient record
    2.Create audit log entry
    3. decrypt encrypted values mask values 
    4. return patient record
    """

    def get(self, request, patient_id):
        try:
            patient = get_object_or_404(PatientRecord.objects.prefetch_related("phones"), 
                                        id=patient_id)
            ip_address = get_ip(request)
            user = request.user if request.user.is_authenticated else None

            try:
                AccessLog.objects.create(
                    patient=patient,
                    accessed_by=user,
                    ip_address=ip_address or "0.0.0.0",
                )
            except Exception:
                pass 

            if not patient and not user:
                return Response(
                {"message": 'Unauthorized', "status":"Error"},
                status=status.HTTP_401_UNAUTHORIZED
                )
            
            masked_ssn = masked_passport = None
            if patient.encrypted_ssn:
                decrypted_ssn = decrypt_value(patient.encrypted_ssn)
                masked_ssn = mask_values({"type":"ssn", "value":decrypted_ssn})
            if patient.encrypted_passport_number:
                decrypted_passport = decrypt_value(patient.encrypted_passport_number)
                masked_passport = mask_values({"type":"passport", "value":decrypted_passport})

            phones = [
            {
                "type": phone.use,
                "number": phone.value,
            }
            for phone in patient.phones.all()
            ]

            response_data = {
            "id": str(patient.id),
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "gender": patient.gender,
            "birth_date": patient.birth_date,
            "ssn": masked_ssn,
            "passport": masked_passport,
            "phones": phones,
            }

            return Response(
                {"message": "Patient details retrieved", "data":response_data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": str(e), "status":"Error", "traceback":str(traceback.format_exc())},
                status=status.HTTP_417_EXPECTATION_FAILED
            )
