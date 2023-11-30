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

<h2>Generating Mpesa Access Token.</h2>
in order to make an API call to Mpesa APIs, we will need to authenticate our app.<br> Safaricom provides an OAuth for generating an access token, which supports client_credentials grant type. <br>Since we will be making an HTTP request to mpesa sandbox, we need a python library to make HTTP requests.


