from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from patient.serializers import PatientSerializer
from patient.helpers import create_patient, create_patient_v2

import logging
logger = logging.getLogger(__name__)


@api_view(['POST'])
def patient_create(request):
    data = request.data
    serializer = PatientSerializer(data=data)
    if serializer.is_valid():
        logger.info('Start create patient pipelines process')
        success, error = create_patient(serializer.validated_data)
        if success:
            logger.info('Success create patient')
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def patient_create_v2(request):
    data = request.data
    serializer = PatientSerializer(data=data)
    if serializer.is_valid():
        logger.info('Start create patient without selenium')
        success, error = create_patient_v2(serializer.validated_data)
        if success:
            logger.info('Success create patient')
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
