
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import *
from .models import User
from random import randint
from django.contrib.auth import authenticate, login
import requests
from rest_framework.views import APIView
from rest_framework import permissions
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
import json
# -------------------------------------------------------------------------------------------------------------------------------
VALIDATION_CODE = 'fdgfdhj67867sdfsf2343nh'
# -------------------------------------------------------------------------------------------------------------------------------
"""
    api's in api_views.py :

    1- GetCSRFToken --> get crrf token for login
    2- login --> login user
    3- user_create  --> create one account with phoneNumber & National Code

"""
# -------------------------------------------------------------------------------------------------------------------------------
@method_decorator(ensure_csrf_cookie, name='dispatch')
class get_csrf_token(APIView):
    """
        Get And Set csrf cookie for FrontEnd(React)
    """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({'success': "CSRF cookie set"})
# -------------------------------------------------------------------------------------------------------------------------------
@api_view(['GET'])
def get_routes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]
    return Response(routes)
# -------------------------------------------------------------------------------------------------------------------------------
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_create(request):
    """
        Create User with Post Api

        Sample json :
        {
        "phoneNumber" : "09303016386",
        "nationalCode" : "0110073754"
        }

    """

    info = UserSerializersValid(data=request.data)
    code = randint(1000, 9999)

    if info.is_valid():
        User(nationalCode=info.validated_data['nationalCode'],
             phoneNumber=info.validated_data['phoneNumber'],
             is_active=False,
             code=code).save()
        # send Code to User
        # temp = Sms_link.replace("phoneNumber",info.validated_data['phoneNumber'])
        # temp = temp.replace("code",str(code))
        # response = requests.get(temp)
        return Response({'message': 'User was created.'}, status=status.HTTP_201_CREATED)
    else:
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
# -------------------------------------------------------------------------------------------------------------------------------
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def code_validation(request):
    """
        It checks whether the code is the same as the code in the database

        Sample json :
        {
        "phoneNumber" : "09303016386",
        "code" : "3387"
        }

    """

    info = CodeValidationSerializers(data=request.data)
    

    if info.is_valid():
        user = User.objects.get(phoneNumber=info.validated_data['phoneNumber'])
        if (user.code == int(info.validated_data['code'])):
            return Response({'message': 'code is right.'}, status=status.HTTP_200_OK)
        return Response({'message': 'wrong code!'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
# -------------------------------------------------------------------------------------------------------------------------------
