from rest_framework import serializers


class ExpenseSummarySerializer(serializers.Serializer):
    category = serializers.CharField()
    amount_sum = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)


class IncomeSummarySerializer(serializers.Serializer):
    source = serializers.CharField()
    amount_sum = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
