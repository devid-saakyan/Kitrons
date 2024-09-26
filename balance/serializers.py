from rest_framework import serializers
from .models import *


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['user', 'available_balance', 'last_withdraw']


class BalanceActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceActivity
        fields = ['user', 'activity_type', 'date', 'views', 'amount']


class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = ['user', 'amount', 'withdraw_date']


