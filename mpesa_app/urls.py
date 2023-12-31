from django.urls import path

from . import views



urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard', views.index, name='index'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),

    
    path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa', views.lipa_na_mpesa_online, name='lipa_na_mpesa_online'),
    path('mpesa/form', views.lipaNaMpesaForm, name='lipa_na_mpesa_form'),
    
    
    path('c2b/register', views.register_urls, name="register_mpesa_validation"),
    
    #path('c2b/transaction_status', views.transaction_status, name="transaction_status"),
    path('c2b/confirmation', views.confirmation, name="confirmation"),
    path('c2b/validation', views.validation, name="validation"),
    path('c2b/callback', views.mpesa_callback, name="call_back"),
    path('c2b/payment', views.payment_request, name="payment_request"),
    path('c2b/qr_code', views.generate_qr_code, name="generate_qr_code"),
    
    path('c2b/mpesa_simulate', views.paybill_online, name="paybill_online"),
]