from django.shortcuts import render
from .models import Balance
from rest_framework import generics

class AvailableBalanceView(generics.GenericAPIView):
    ...

