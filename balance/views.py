from .models import *
from .serializers import BalanceSerializer
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import BalanceActivity
from .serializers import BalanceActivitySerializer
from django.utils.dateparse import parse_date
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GetAvailableBalance(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT Token", type=openapi.TYPE_STRING),
            openapi.Parameter('Language', openapi.IN_HEADER, description="Language", type=openapi.TYPE_STRING),
            openapi.Parameter('DeviceToken', openapi.IN_HEADER, description="Device Token", type=openapi.TYPE_STRING),
            openapi.Parameter('OsType', openapi.IN_HEADER, description="Operating System Type",
                              type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        try:
            balance = Balance.objects.get(user=request.user)
        except Balance.DoesNotExist:
            balance = Balance.objects.create(user=request.user, available_balance=0.0)
        total_activity_amount = BalanceActivity.objects.filter(user=request.user).aggregate(
            total_amount=Sum('amount')
        )['total_amount'] or 0.0
        total_withdrawn = Withdraw.objects.filter(user=request.user).aggregate(
            total_withdrawn=Sum('amount')
        )['total_withdrawn'] or 0.0
        available_balance = total_activity_amount - total_withdrawn
        balance.available_balance = available_balance
        balance.save()
        serializer = BalanceSerializer(balance)
        return Response(serializer.data)


class GetBalancesByDate(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Language', openapi.IN_HEADER, description="Language", type=openapi.TYPE_STRING),
            openapi.Parameter('DeviceToken', openapi.IN_HEADER, description="Device Token", type=openapi.TYPE_STRING),
            openapi.Parameter('OsType', openapi.IN_HEADER, description="Operating System Type",
                              type=openapi.TYPE_STRING),
        ]
    )
    def post(self, request, *args, **kwargs):
        date_from = request.data.get('DateFrom')
        date_to = request.data.get('DateTo')
        date_from = parse_date(date_from)
        date_to = parse_date(date_to)
        activities = BalanceActivity.objects.filter(user=request.user, date__gte=date_from, date__lte=date_to)
        serializer = BalanceActivitySerializer(activities, many=True)
        return Response(serializer.data)


class GetBalancesByActivity(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Language', openapi.IN_HEADER, description="Language", type=openapi.TYPE_STRING),
            openapi.Parameter('DeviceToken', openapi.IN_HEADER, description="Device Token", type=openapi.TYPE_STRING),
            openapi.Parameter('OsType', openapi.IN_HEADER, description="Operating System Type",
                              type=openapi.TYPE_STRING),
        ]
    )
    def post(self, request, *args, **kwargs):
        activity_type = request.data.get('ActivityType')
        activities = BalanceActivity.objects.filter(user=request.user, activity_type=activity_type)
        serializer = BalanceActivitySerializer(activities, many=True)
        return Response(serializer.data)