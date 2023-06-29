# Generated by Django 4.1.5 on 2023-06-29 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QRCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('response_code', models.CharField(max_length=100)),
                ('request_id', models.CharField(max_length=100)),
                ('response_description', models.CharField(max_length=255)),
                ('qr_code', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('merchant_name', models.CharField(max_length=100)),
                ('ref_no', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('trx_code', models.CharField(max_length=10)),
                ('cpi', models.CharField(max_length=100)),
                ('size', models.CharField(max_length=10)),
                ('qr_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mpesa_app.qrcode')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
    ]
