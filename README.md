# mpesa-daraja-Api
working with mpesa daraja Api, C2B
## mpesa - daraja api 
Requirements for this project <br>

First you need to have registered in safaricom dev. follow <a href ="https://developer.safaricom.co.ke/"> this link </a><br>
create your app. To get started, create an app on Sandbox. You can copy your credentials<br>
have python installed.<br>
install django using pip.<br>
pip install django-mpesa<br>
a good computer and basic python  understanding.<br>
a cup of coffee and we are good to go.<br>

<h2>** Running this project**</h2>
django-admin startproject mysite<br>
cd mysite.<br>
python manage.py runserver.<br>
we can see that our website is up and running on localhost/<br>
You have 18 unapplied migrations. now lets run command.<br>

<h2>Generating Mpesa Access Token.</h2> <a href="https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"> api url</a>
In order to make an API call to Mpesa APIs, we will need to authenticate our app.<br> Safaricom provides an OAuth for generating an access token, which supports client_credentials grant type.<br> This API generates the tokens for authenticating your API calls. This is the first API you will engage with within the set of APIs available because all the other APIs require authentication information from this API to work.
<br>Since we will be making an HTTP request to mpesa sandbox, we need a python library to make HTTP requests.

<h2> Getting started</h2>

// we are going to use python request library.<br>
 pip install requests<br>
//so far so good.
A sample code for generating and validating access token  in python.<br>
def getAccessToken(request):<br>
    consumer_key = 'your key'<br>
    consumer_secret = 'your consumer secret key'<br>
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'<br>

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))<br>
    mpesa_access_token = json.loads(r.text)<br>
    validated_mpesa_access_token = mpesa_access_token['access_token']<br>

    return HttpResponse(validated_mpesa_access_token)<br>
<h3>stk push intergration</h3><br>
For detailed explanation follow the safaricom <br>
// working with postman. <br>
Download and install postman <br>
Used to test and access APIs.




