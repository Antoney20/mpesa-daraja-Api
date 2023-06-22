from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'


class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'


class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'

    def __str__(self):
        return self.first_name

class QRCode(models.Model):
    response_code = models.CharField(max_length=100)
    request_id = models.CharField(max_length=100)
    response_description = models.CharField(max_length=255)
    qr_code = models.TextField()

    def __str__(self):
        return f'Response Code: {self.response_code}, Request ID: {self.request_id}'

class Payment(models.Model):
    merchant_name = models.CharField(max_length=100)
    ref_no = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    trx_code = models.CharField(max_length=10)
    cpi = models.CharField(max_length=100)
    size = models.CharField(max_length=10)
    qr_code = models.ForeignKey(QRCode, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Ref No: {self.ref_no}, Amount: {self.amount}'
