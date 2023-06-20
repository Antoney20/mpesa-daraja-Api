from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.http import HttpResponse
import requests
from django.http import HttpResponse, JsonResponse
from requests.auth import HTTPBasicAuth
from . credentials import MpesaAccessToken, LipanaMpesaPassword
from .models import MpesaPayment
import json


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



@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPassword.Business_short_code,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://mydomain.com/confirmation",
               "ValidationURL": "https://mydomain.com/validation"}
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
    return JsonResponse(dict(context))