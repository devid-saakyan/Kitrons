from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from company.models import Company
from company.serializers import CompanySerializer1


class GetCompanyList(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer1

    def get(self, request, *args, **kwargs):
        companies = self.get_queryset()
        serializer = self.get_serializer(companies, many=True)
        return Response({
            'success': True,
            'data': {
                'data': serializer.data
            }
        })


class GetCompanyById(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer1

    def get(self, request, *args, **kwargs):
        company_id = self.kwargs.get('pk')
        try:
            company = self.get_queryset().get(id=company_id)
            serializer = self.serializer_class(company)
            return Response({
                'success': True,
                'data': {
                    'data': [serializer.data]
                }
            })
        except Company.DoesNotExist:
            return Response({'success': False, 'message': 'Company not found'})