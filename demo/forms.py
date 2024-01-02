from django import forms
from .models import Member
from .models import transactions
from .models import payments


class MemberForm(forms.ModelForm):
    class Meta:
        model=Member
        fields='__all__'

class TransactionsForm(forms.ModelForm):
    class Meta:
        model=transactions
        fields='__all__'
    
class PaymentsForm(forms.ModelForm):
    class Meta:
        model=payments
        fields='__all__'

