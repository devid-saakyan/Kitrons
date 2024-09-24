from django.urls import path
from .views import *

urlpatterns = [
    path('Login/', LoginView.as_view(), name='login'),
    path('VerifyPhoneNumber/', VerifyPhoneView.as_view(), name='verify_phone'),
    path('VerifyEmail/', VerifyEmailView.as_view(), name='verify_email'),
    path('SendPhoneCode/<str:phone>', SendPhoneCodeView.as_view(), name='send_phone_code'),
    path('SendEmailCode/<str:email>', SendEmailCodeView.as_view(), name='send_email_code'),
]
