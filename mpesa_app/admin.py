from django.contrib import admin

# Register your models here.
from .models import MpesaPayment,QRCode,Payment,MpesaCallBacks,MpesaCalls

admin.site.register(MpesaPayment)
admin.site.register(MpesaCalls)
admin.site.register(MpesaCallBacks)
admin.site.register(QRCode)
admin.site.register(Payment)

