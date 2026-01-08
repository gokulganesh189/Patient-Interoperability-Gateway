from rest_framework import serializers
from datetime import date, datetime


class PatientIntakeSerializer(serializers.Serializer):

    resourceType = serializers.CharField()
    birthDate = serializers.CharField()
    identifier = serializers.ListField(
        child=serializers.DictField(),
        required=False
    )

    def validate(self, data):
        if data.get("resourceType").lower() != "patient":
            raise serializers.ValidationError(
                {"resourceType": "resourceType must be 'Patient'"}
            )
        
        birth_date_str = data.get("birthDate")

        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        except ValueError:
            raise serializers.ValidationError(
                {"birthDate": "birthDate must be in YYYY-MM-DD format"}
            )
        
        today = date.today()
        age = today.year - birth_date.year - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )

        if age < 18:
            raise serializers.ValidationError(
                {"birthDate": "Patient must be at least 18 years old"}
            )
        
        ssn = None
        passport = None

        for ident in data.get("identifier", []):
            system = ident.get("system")
            value = ident.get("value")

            if system == "http://hl7.org/fhir/sid/us-ssn":
                ssn = value
            elif system == "http://hl7.org/fhir/sid/passport":
                passport = value
        
        data["ssn"] = ssn
        data["passport"] = passport
        data['parsed_birth_date'] = birth_date

        return data
