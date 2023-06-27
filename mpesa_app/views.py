from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import requires_csrf_token

# Create your views here.
from django.http import HttpResponse
import requests
from django.http import HttpResponse, JsonResponse
from requests.auth import HTTPBasicAuth
from . credentials import MpesaAccessToken, LipanaMpesaPassword, MpesaPaybill
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

# Lipa na mpesa.  c2b
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
        "PartyA": 254748181420,  
        "PartyB": LipanaMpesaPassword.Business_short_code,
        "PhoneNumber": 254748181420,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Antony",
        "TransactionDesc": "Testing stk push"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse(response.text)

#Payment online. Paybill. mpesa express /mpesa_simulate
def paybill_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {'Authorization': f'Bearer {access_token}', 
               'Content-Type': 'application/json'}
    request = {
        "BusinessShortCode": MpesaPaybill.Business_short_code,
        "Password": MpesaPaybill.decode_password,
        "Timestamp": MpesaPaybill.date_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254792193714,  
        "PartyB": 174379,
        "PhoneNumber": 254792193714,  # replace with your phone number to get st
        "CallBackURL": "https://bc3c-41-90-249-79.ngrok-free.app/app/v1/c2b/callback",
        "AccountReference": "Antony-Test",
        "TransactionDesc": "Payment of X"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse(response.text)


@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPassword.Test_c2b_shortcode,
               "ResponseType": "Cancelled/Completed",
                "ConfirmationURL": "https://60b3-41-90-249-79.ngrok-free.app/api/v1/c2b/confirmation",
               "ValidationURL": "https://60b3-41-90-249-79.ngrok-free.app/api/v1/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)
@csrf_exempt
def call_back(request):
    data = json.loads(request.body)

    # Extract relevant information from the data
    result_code = data['Body']['stkCallback']['ResultCode']
    result_desc = data['Body']['stkCallback']['ResultDesc']

    # Check if the transaction was successful or unsuccessful
    if result_code == 0:
        # Successful transaction
        response_body = {
            "Body": {
                "stkCallback": {
                    "MerchantRequestID": data['Body']['stkCallback']['MerchantRequestID'],
                    "CheckoutRequestID": data['Body']['stkCallback']['CheckoutRequestID'],
                    "ResultCode": result_code,
                    "ResultDesc": result_desc,
                    "CallbackMetadata": {
                        "Item": [
                            {"Name": "", "Value": 1},
                            {"Name": "", "Value": ""}
                        ]
                    }
                }
            }
        }
    else:
        # Unsuccessful transaction
        response_body = {
            "Body": {
                "stkCallback": {
                    "MerchantRequestID": data['Body']['stkCallback']['MerchantRequestID'],
                    "CheckoutRequestID": data['Body']['stkCallback']['CheckoutRequestID'],
                    "ResultCode": result_code,
                    "ResultDesc": result_desc
                }
            }
        }

    # Send the response to M-Pesa API
    return HttpResponse(json.dumps(response_body), content_type='application/json')

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
    print(mpesa_body)
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

#generating QR code.
def generate_qr_code(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/qrcode/v1/generate'
    headers = {"Authorization": "Bearer %s" % access_token}

    request_data = {
        'MerchantName': 'TEST SUPERMARKET',
        'RefNo': 'Payment Test',
        'Amount': 1,
        'TrxCode': 'BG',  #Transaction Type. The supported types are:
        #BG: Pay Merchant (Buy Goods).
        #WA: Withdraw Cash at Agent Till....
         #PB: Paybill or Business number.
        'CPI': '254792193714', #Credit Party Identifier. Can be a Mobile Number, Business Number, Agent Till, Paybill or Business number
        'Size': '300' #Size of the QR code image in pixels
    }

    response = requests.post(api_url, json=request_data, headers=headers)

    return HttpResponse(response.text)

    
    # payment request /payment
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
        'QueueTimeOutURL': 'https://mydomain.com/b2c/queue',
        'ResultURL': 'https://mydomain.com/b2c/result',
        'Occasion': 'Hey antony. tihs is your payment'
    }

    response = requests.post(api_url, json=request_data, headers=headers)

    if response.status_code == 200:
        # Payment request was successful
        response_data = response.json()
        transaction_id = response_data['ConversationID']
        return HttpResponse(response.text)
    else:
        # Payment request failed
        return HttpResponse(response.text)
    
    