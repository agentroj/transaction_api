# transactions_app/serializers.py

from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    transaction_type = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    # allow_blank=True so DRF won't reject "" before our custom check
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = Transaction
        fields = ['id',
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

    def validate(self, data):
        raw = self.initial_data.get('description')
        if not isinstance(raw, str):
            raise serializers.ValidationError(
                {'description': ['description must be a string']
                 })
        text = raw.strip()
        if text == "":
            raise serializers.ValidationError(
                {'description': ['description cannot be empty']}
                )
        if len(text) > 500:
            raise serializers.ValidationError(
                {'description': ['description cannot exceed 500 characters']}
                )
        return data
