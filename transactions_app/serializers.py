from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'transaction_type',
            'amount',
            'description',
            'created_at'
            ]

    def validate_transaction_type(self, value):
        if value not in dict(Transaction.TRANSACTION_TYPES):
            raise serializers.ValidationError(
                "transaction_type must be either DEPOSIT or WITHDRAWAL"
            )
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("amount must be positive (> 0)")
        return value

    def validate_description(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("description must be a string")
        text = value.strip()
        if not text:
            raise serializers.ValidationError("description cannot be empty")
        if len(text) > 500:
            raise serializers.ValidationError(
                "description cannot exceed 500 characters"
                )
        return text
