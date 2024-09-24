from rest_framework import generics
from rest_framework.response import Response
from .models import Balance
from ads.models import Ad
from .serializers import BalanceDateRangeSerializer, BalanceActivitySerializer, UserBalanceActivitySerializer
from django.db.models import Sum, Count
from datetime import datetime


class AvailableBalanceView(generics.GenericAPIView):
    def get(self, request):
        balances = Balance.objects.filter(user=self.request.user)
        balance_activities = []

        for balance in balances:
            activity = {
                "count": 1,  # У нас одно значение баланса на каждую запись
                "amount": balance.available_balance,
                "date": balance.date
            }
            balance_activities.append(activity)

        response_data = {"userBalanceActivities": balance_activities}
        return Response(response_data)


class BalanceByDateView(generics.GenericAPIView):
    serializer_class = BalanceDateRangeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            date_from = serializer.validated_data['date_from']
            date_to = serializer.validated_data['date_to']
            balances = Balance.objects.filter(user=request.user, date__range=[date_from, date_to])

            balance_activities = []

            for balance in balances:
                activity = {
                    "count": 1,
                    "amount": balance.available_balance,
                    "date": balance.date
                }
                balance_activities.append(activity)

            response_data = {"userBalanceActivities": balance_activities}
            return Response(response_data)
        return Response(serializer.errors, status=400)


class BalanceByActivityView(generics.GenericAPIView):
    serializer_class = BalanceActivitySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            date_from = serializer.validated_data['date_from']
            date_to = serializer.validated_data['date_to']
            category = serializer.validated_data['category']
            ads = Ad.objects.filter(category=category)
            balances = Balance.objects.filter(user=request.user, date__range=[date_from, date_to])

            balance_activities = []

            for balance in balances:
                activity = {
                    "count": 1,
                    "amount": balance.available_balance,
                    "date": balance.date
                }
                balance_activities.append(activity)

            response_data = {"userBalanceActivities": balance_activities}
            return Response(response_data)
        return Response(serializer.errors, status=400)
