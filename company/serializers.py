from rest_framework import serializers
from .models import *

class CompanySerializer1(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'