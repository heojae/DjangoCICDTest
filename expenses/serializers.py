from rest_framework import serializers
from expenses.models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['date', 'id', 'description', 'amount', 'category']

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data=validated_data)
