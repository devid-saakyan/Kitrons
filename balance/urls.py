from django.urls import path
from .views import GetAvailableBalance, GetBalancesByDate, GetBalancesByActivity

urlpatterns = [
    path('GetAvailableBalance', GetAvailableBalance.as_view(), name='get_available_balance'),
    path('GetBalancesByDate', GetBalancesByDate.as_view(), name='get_balances_by_date'),
    path('GetBalancesByActivity', GetBalancesByActivity.as_view(), name='get_balances_by_activity'),
]
