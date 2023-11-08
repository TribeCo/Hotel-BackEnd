
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
from config.settings import hotel_email,password_email
from email.message import EmailMessage
import smtplib
import random
# -------------------------------------------------------------------------------------------------------------------------------
VALIDATION_CODE = 'fdgfdhj67867sdfsf2343nh'
# -------------------------------------------------------------------------------------------------------------------------------
"""
    api's in api_views.py :

    1- GetCSRFToken --> get crrf token for login
    2- login --> login user
    3- user_create  --> create one account with email & National Code
    4- code_validation --> It checks whether the code is the same as the code in the database
    5- user_update --> Update User information 

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
def get_endpoint(request):
    endpoints = [
        '/api/token',
        '/api/token/refresh',
        'user/create/'
    ]

    return Response(endpoints)
# -------------------------------------------------------------------------------------------------------------------------------
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_create(request):
    """
        Create User with Post Api

        Sample json :
        {
        "email" : "TahaM8000@gmail.com",
        "nationalCode" : "0112037754"
        }

    """

    info = UserSerializersValid(data=request.data)
    code = randint(1000, 9999)

    if info.is_valid():
        user = User(nationalCode=info.validated_data['nationalCode'],
             email=info.validated_data['email'],
             is_active=False,
             code=code).save()
        # send Code to User
        
        msg = EmailMessage()
        msg['Subject'] = 'کد اعتبار سنجی سایت هتل'
        msg['From'] = hotel_email
        msg['To'] = user.email
        msg.set_content(f"کد شما: {user.code}")

        with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
            server.login(hotel_email,password_email)
            server.send_message(msg)
        
        return Response({'message': 'User was created and code send.'}, status=status.HTTP_201_CREATED)
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
        "email" : "TahaM8000@gmail.com",
        "code" : "3387"
        }

    """

    info = CodeValidationSerializers(data=request.data)
    

    if info.is_valid():
        user = User.objects.get(email=info.validated_data['email'])
        if (user.code == int(info.validated_data['code'])):
            
            user.is_active = True
            user.save()
            return Response({'message': 'code is right.'}, status=status.HTTP_200_OK)
        return Response({'message': 'wrong code!'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
# -------------------------------------------------------------------------------------------------------------------------------
from django.http import JsonResponse
from django.conf import settings
import jwt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_update(request):
    """
    Update User information

    Sample json :
    {
        "email" : "TahaM8000@gmail.com",
        "firstName" : "Taha",
        "lastName" : "Mousavi",
        "password" : "1234jj5678"
    }

    """

    token = request.headers.get('Authorization')

    if not token:
        return JsonResponse({'error': 'Access denied. No token provided.'}, status=401)
    
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.InvalidTokenError:
        return JsonResponse({'error': 'Invalid token.'}, status=401)

    user_email = decoded_token.get('email')

    
    info = UserSerializersUpdate(data=request.data)


    if info.is_valid():
        try:
            user = User.objects.get(email=info.validated_data['email'])
        except User.DoesNotExist:
            return Response({'error': 'this user does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if user_email != info.validated_data['email']:
            return JsonResponse({'error': 'Access denied. User mismatch.'}, status=403)

        user.firstName = info.validated_data['firstName']
        user.lastName = info.validated_data['lastName']

        user.set_password(info.validated_data['password'])

        # Do the rest of the process of adding information here


        #...
        
        user.save()
        return Response({'message': 'ok is updated'}, status=status.HTTP_200_OK)
    else:
        return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
# -------------------------------------------------------------------------------------------------------------------------------
        


# -------------------------------------------------------------------------------------------------------------------------------



    

    

    
