# Generated by Django 4.1.5 on 2023-06-29 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa_app', '0004_delete_mpesacallsnew'),
    ]

    operations = [
        migrations.CreateModel(
            name='MpesaCallsNew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ip_address', models.TextField()),
                ('caller', models.TextField()),
                ('conversation_id', models.TextField()),
                ('MerchantRequestID', models.TextField()),
                ('CheckoutRequestID', models.TextField()),
                ('ResponseCode', models.TextField()),
                ('ResponseDescription', models.TextField()),
                ('CustomerMessage', models.TextField()),
                ('content', models.TextField()),
            ],
            options={
                'verbose_name': 'Mpesa Call',
                'verbose_name_plural': 'Mpesa Calls',
            },
        ),
    ]
