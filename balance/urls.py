from django.urls import path
from .views import AvailableBalanceView, BalanceByDateView, BalanceByActivityView

urlpatterns = [
    path('get-available-balance/', AvailableBalanceView.as_view(), name='get_available_balance'),
    path('get-balances-by-date/', BalanceByDateView.as_view(), name='get_balances_by_date'),
    path('get-balances-by-activity/', BalanceByActivityView.as_view(), name='get_balances_by_activity'),
]
