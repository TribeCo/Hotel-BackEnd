from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User,Payments
from config.settings import merchant
#------------------------------------------------------------------------------------------------
messages_dict = {
    "not_order" : 'جنین سفارشی در دیتابیس وجود ندارد.',
    "not_connected" : ' اتصال به درگاه ناموفق بود.',
    "too_long" : 'زمان بیش حد سپری شده برای اتصال به درگاه.',
    "not_success_connect" : 'اتصال ناموفق.',
    "success" : 'خرید با موفقیت انجام شد.',
    "payed" : 'پرداخت انجام شده بوده است.',
    "not_success_connect" : 'پرداخت ناموفق بود.',
    "not_upload" : 'آپلود با مشکل مواجه شد.',
    "success_upload" : "آپلود با موفقیت انجام شد. برای پیگیری سفارش به داشبورد مراجعه کنید.",
}

color_messages = {
    "error" : 'background-color: rgb(198, 2, 2);',
    "success" : 'background-color: rgb(0, 190, 0);',
    "gray" : 'background-color: rgb(108, 105, 105);',
}
#-----------------------------------------------------------------------------------
"""
    this file is for connecting to Banking portal.
        
"""
#-----------------------------------------------------------------------------------
"""
    this block for config with ZarinPal portal.
"""
from django.http import HttpResponse
import requests
import json

if True:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

MERCHANT = merchant
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
# amount = 11000  # Rial / Required
description = "هتل"  # Required
email = 'fiveplusone.ir@gmail.com'  # Optional
# mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/api/verify/' #Change thiiiiiiiiiiiiiiiis to front

user_id = 1450
user = None
#-----------------------------------------------------------
class PayMoneyAPIView(APIView):
    """
        Create a link for redirecting user to portal bank.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):

        global user_id
        user = request.user
        user_id = user.id

        amount = user.total_price()
        # print(amount)


        data = {
            "MerchantID": MERCHANT,
            "Amount": amount,
            "Description": description,
            "Phone": user.id,
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        try:
            response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

            
            response_dict = json.loads(response.text)
            print(response_dict)
            status = response_dict['Status']
            authority = response_dict['Authority']


            if(status == 100):
                redirect_url = f"{ZP_API_STARTPAY}{authority}"
                return Response({'redirect_url':redirect_url,})
            print(status)
            return Response({'message':messages_dict['not_connected'],})


        
        except requests.exceptions.Timeout:
            return Response({'message':messages_dict['too_long'],})
        except requests.exceptions.ConnectionError:
            return Response({'message':messages_dict['not_success_connect'],})
        
#-----------------------------------------------------------
class VerifyAPIView(APIView):
    """
        This api checks whether the payment has been made correctly or not.
    """
    def get(self, request):
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']

        global user_id
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message':messages_dict['not_order'],})

        amount = user.total_price()

        
        if(t_status == "NOK"):
            return Response({'message':messages_dict['not_success_connect'],})
        
        elif(t_status == "OK"):
            data = {
                "MerchantID": MERCHANT,
                "Amount": amount,
                "Authority": t_authority,
            }
        
            data = json.dumps(data)
            # set content length by data
            headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
            response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

            response_dict = json.loads(response.text)
            status = response_dict['Status']
            RefID = response_dict['RefID']

            if status == 100:
                    user.all_payed()
                    pay_obj = Payments(ref_id = RefID,
                    authority = t_authority,
                    user = user,
                    amount = amount
                    )
                    pay_obj.save()
                    user.save()
                                
                    return Response({'message':messages_dict['success'],})

            elif status == 101:
                return Response({'message':messages_dict['payed'],})

            else:
                return Response({'message':messages_dict['not_success_connect'],})
        else:
            return Response({'message':messages_dict['not_success_connect'],})
#-----------------------------------------------------------