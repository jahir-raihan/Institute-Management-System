from django import forms
from .models import TransactionDetails


class ReasonSelectorForm(forms.ModelForm):
    class Meta:
        model = TransactionDetails
        fields = ['transaction', 'transaction_reason', 'transaction_amount']
