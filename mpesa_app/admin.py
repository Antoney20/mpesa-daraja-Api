from django.contrib import admin

# Register your models here.
from .models import MpesaPayment,QRCode,Payment,MpesaCallBacks,MpesaCallsNew

admin.site.register(MpesaPayment)
admin.site.register(MpesaCallsNew)
admin.site.register(MpesaCallBacks)
admin.site.register(QRCode)
admin.site.register(Payment)

