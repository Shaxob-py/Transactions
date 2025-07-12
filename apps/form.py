from wsgiref.util import request_uri

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, forms, CharField, PasswordInput, Form

from apps.models import Transaction


class AddTransactionModelForm(ModelForm):
    class Meta:
        model = Transaction
        fields = 'amount', 'type', 'category', 'date'

    def clean(self):
        clean_data = self.cleaned_data
        translation = clean_data.get('translation')
        type = clean_data.get('type')
        amount = clean_data.get('amount')

        if type == Transaction.TransactionType.INCOME:
            Transaction.total_income += amount
        if type == Transaction.TransactionType.EXPENSE:
            Transaction.total_income += amount
        return clean_data


class AuthRegisterMoelForm(ModelForm):
    class Meta:
        model = User
        fields = 'username', 'email', 'password', 'first_name', 'last_name'

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already in use.')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 5:
            raise ValidationError('This password is too short.')
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginModelForm(Form):
    username = CharField(required=True)
    password = CharField(widget=PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError('Invalid username or password.')
        self.user = user
        return cleaned_data
