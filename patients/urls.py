from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import path
from . import views

urlpatterns = [

    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("patient-intake/",views.PatientIntakeView.as_view(),name="patient-intake"),
    path("patients/<uuid:patient_id>/",views.PatientDetailView.as_view(),name="patient-detail"),
]
