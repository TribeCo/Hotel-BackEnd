
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
Sms_link = 'http://www.0098sms.com/sendsmslink.aspx?FROM=300057341485&TO=phoneNumber&TEXT=کد+:+code&USERNAME=smsa5429&PASSWORD=66578289&DOMAIN=0098'
# -------------------------------------------------------------------------------------------------------------------------------
"""
    api's in api_views.py :

    1- GetCSRFToken --> get crrf token for login
    2- login --> login user

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
