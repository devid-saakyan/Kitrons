from rest_framework import serializers
from .models import Balance


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'


class BalanceDateRangeSerializer(serializers.Serializer):
    date_from = serializers.DateField()
    date_to = serializers.DateField()


class BalanceActivitySerializer(serializers.Serializer):
    date_from = serializers.DateField()
    date_to = serializers.DateField()
    category = serializers.ChoiceField(choices=[('video', 'Video'),
                                                ('story', 'Story'),
                                                ('post', 'Post')])


class UserBalanceActivitySerializer(serializers.Serializer):
    count = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    date = serializers.DateTimeField()