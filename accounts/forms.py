from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.validators import validate_email
from django.db.models import Q

from .models import Accounts


class AccountForm(UserCreationForm):
    class Meta:
        model = Accounts
        fields = [
            'first_name',
            'last_name',
            'email',
            'mobile',
            'gender',
            'parent_id',
            'address',
            'aadhar_card',
            'pan_number',
        ]

    def clean(self):
        mobile = self.cleaned_data.get('mobile')
        email = self.cleaned_data.get('email')
        parent = self.cleaned_data.get('parent_id', None)

        if len(mobile) != 10 or not mobile.isnumeric():
            raise forms.ValidationError("Invalid mobile")
        validate_email(email)

        print(Accounts.objects.filter(Q(mobile=mobile) | Q(email=email)))
        if Accounts.objects.filter(Q(mobile=mobile) | Q(email=email)):
            raise forms.ValidationError("User Exist")

        if len(Accounts.objects.filter(referral_code=parent)) != 1 or None:
            raise forms.ValidationError("Invalid DsID")
        return self.cleaned_data
