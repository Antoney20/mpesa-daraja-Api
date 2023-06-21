from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import requires_csrf_token

# Create your views here.
from django.http import HttpResponse
import requests
from django.http import HttpResponse, JsonResponse
from requests.auth import HTTPBasicAuth
from . credentials import MpesaAccessToken, LipanaMpesaPassword
from .models import MpesaPayment
import json

from django.contrib.auth import logout
from django.shortcuts import redirect

from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return render(request, 'mpesa_app/index.html')
    return render(request, 'mpesa_app/register.html'
                  )
def index(request):
    return render(request, 'mpesa_app/index.html')

def login(request):
    return render(request, 'mpesa_app/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def forgot_password(request):
  
    return render(request, 'mpesa_app/forgot_password.html')
def lipaNaMpesaForm(request):
    return render(request, 'mpesa_app/lipa_na_mpesa_form.html')

def getAccessToken(request):
    consumer_key = 'jZZ1Izq3fr2ZB4jg0Kv6GAXy41G7d4ZG'
    consumer_secret = 'lghIvsY5Fkz7zXl3'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)

def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    request = {
        "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
        "Password": LipanaMpesaPassword.decode_password,
        "Timestamp": LipanaMpesaPassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254792193714,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPassword.Business_short_code,
        "PhoneNumber": 254792193714,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Antony",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')

import requests
from requests.auth import HTTPBasicAuth

def payment_request(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'

    headers = {
        'Authorization': f'Bearer {access_token}','Content-Type': 'application/json'}

    request_data = {
        'InitiatorName': 'ANTONY',
        'SecurityCredential': 'enF4l6Cv+1GEZiURsG00ycbwoNg46Q/cx6zeFbeNvkJcgGBrBku3gKcNDmJ8lk0NGqzzXMxgv8uaBSnhSRgE7s9gTEQ2sZ/spOHcGo9kJ8/XSLakxOvWjKdsvuV9T91LWWSuVGP19xOvmU15CfE2pccD24q+0KjDbJ7iCyLY09Gry0zprT/X/7TsWBsZaSMk3uc3KE91a8tahueOfYiSAKjYp7yUnaYPOvMriq03oSYz58Bnh+eWK9BU0CRCH5IrE4ZqNHYR6wsX+CXl+NAmdfzcIgfE1IfAf0C+YKLiZ4flI+FZbcuSWcP8EkfIIHWNrsLmGyYijt3456y3DSnMeA==',
        'CommandID': 'SalaryPayment',
        'Amount': 1,
        'PartyA': 600983,
        'PartyB': 254792193714,
        'Remarks': 'salary payment',
        'QueueTimeOutURL': 'YOUR_QUEUE_TIMEOUT_URL',
        'ResultURL': 'YOUR_RESULT_URL',
        'Occasion': 'YOUR_OCCASION'
    }

    response = requests.post(api_url, json=request_data, headers=headers)

    if response.status_code == 200:
        # Payment request was successful
        response_data = response.json()
        transaction_id = response_data['ConversationID']
        return transaction_id
    else:
        # Payment request failed
        return HttpResponse(response.text)


@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPassword.Test_c2b_shortcode,
               "ResponseType": "Completed",
                "ConfirmationURL": "https://6610-41-90-249-79.ngrok-free.app/api/v1/c2b/confirmation",
               "ValidationURL": "https://6610-41-90-249-79.ngrok-free.app/api/v1/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)
@csrf_exempt
def call_back(request):
    pass
@csrf_exempt
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))
@csrf_exempt
def confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],
    )
    payment.save()
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return HttpResponse(response.text)