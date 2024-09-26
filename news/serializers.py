from rest_framework import serializers
from .models import *
from company.serializers import CompanySerializer1


class NewsListSerializer(serializers.ModelSerializer):
    company = CompanySerializer1()

    class Meta:
        model = News
        fields = '__all__'
