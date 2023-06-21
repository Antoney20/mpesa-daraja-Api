from django import forms
from .models import MpesaPayment

class LipaNaMpesaForm(forms.ModelForm):
    class Meta:
        model = MpesaPayment
        fields = ('amount', 'description', 'type', 'reference', 'first_name', 'middle_name', 'last_name', 'phone_number', 'organization_balance')
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'organization_balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }
