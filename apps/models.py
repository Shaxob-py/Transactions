from django.db import models
from django.db.models import TextChoices, Model, CharField, DateField, TextField, DecimalField


class Transaction(Model):
    class TransactionType(TextChoices):
        INCOME = 'Income' , 'income'
        EXPENSE = 'Expense' , 'expense'

    type = CharField(max_length=10, choices=TransactionType.choices,null=True , blank=True)  # noqa
    date = DateField(null=True , blank=True)
    category = CharField(max_length=25, default=0,null=True , blank=True)
    total_income = DecimalField(max_digits=10, decimal_places=0, default=0)
    amount = DecimalField(max_digits=10, decimal_places=0, default=0)
    total_expense = DecimalField(max_digits=10, decimal_places=0, default=0)
    total_balance = DecimalField(max_digits=10, decimal_places=0, default=0)

