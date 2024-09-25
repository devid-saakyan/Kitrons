from django.shortcuts import render
from rest_framework import generics

from company.models import Company
from company.serializers import CompanySerializer1


class GetCompanyList(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer1


class GetCompanyById(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer1