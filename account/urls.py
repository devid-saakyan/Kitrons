from django.urls import path
from .views import LoginView, VerifyPhoneView, VerifyEmailView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('verify-phone/', VerifyPhoneView.as_view(), name='verify_phone'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
]
