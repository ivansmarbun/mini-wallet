from django.db import models
import uuid
from django.db.models.base import Model
from django.db import transaction
from django.utils.crypto import get_random_string
import datetime


class CustomerWallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_xid = models.CharField(max_length=126, unique=True)
    token = models.CharField(max_length=32)
    status = models.BooleanField(default=False)
    enable_at = models.DateTimeField(null=True)
    disable_at = models.DateTimeField(null=True)
    balance = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding == True:
            self.token = get_random_string(length=32)
            self.enable_at = datetime.datetime.now()
        super(CustomerWallet, self).save(*args, **kwargs)

    def enable_wallet(self):
        if self.status:
            return False
        else:
            self.status = True
            self.enable_at = datetime.datetime.now()
            self.save()
            return True

    def disable_wallet(self):
        self.status = False
        self.disable_at = datetime.datetime.now()
        self.save()

    @classmethod
    def deposit(cls, token, amount):
        with transaction.atomic():
            customer_wallet = (
                cls.objects
                .select_for_update()
                .get(token=token)
            )
            customer_wallet.balance += amount
            customer_wallet.save()

    @classmethod
    def withdraw(cls, token, amount):
        with transaction.atomic():
            customer_wallet = (
                cls.objects
                .select_for_update()
                .get(token=token)
            )
            if customer_wallet.balance < amount:
                return False
            customer_wallet.balance -= amount
            customer_wallet.save()
            return True


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        DEPOSIT = 'D', 'Deposit'
        WITHDRAW = 'W', 'Withdraw'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_wallet = models.ForeignKey(
        CustomerWallet, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=1, choices=TransactionType.choices)
    amount = models.FloatField(default=0)
    transaction_date = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=126, null=False, unique=True)
    status = models.BooleanField(default=True)
