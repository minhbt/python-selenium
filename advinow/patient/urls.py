from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from patient import views

urlpatterns = [
    path('patients/', views.patient_create),
    path('v2/patients/', views.patient_create_v2)
]

urlpatterns = format_suffix_patterns(urlpatterns)