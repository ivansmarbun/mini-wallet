from rest_framework import serializers


class CreateWalletSerializer(serializers.Serializer):
    customer_xid = serializers.CharField(required=True)


class TransactionSerializer(serializers.Serializer):
    reference_id = serializers.CharField(required=True)
    amount = serializers.FloatField(required=True)
