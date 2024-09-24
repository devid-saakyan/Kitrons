from rest_framework import serializers
from .models import *
from company import models


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseAd
        fields = '__all__'


class AdDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseAd
        fields = ['id', 'title', 'description', 'company', 'category', 'created_at']


class UserAdHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAdHistory
        fields = '__all__'


class ApplyAnswerSerializer(serializers.Serializer):
    answerId = serializers.IntegerField()
    questionId = serializers.IntegerField()
    adsId = serializers.IntegerField()


class AdAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdAnswer
        fields = ['id', 'question', 'answer_text', 'is_correct']


class AdQuestionResponseSerializer(serializers.ModelSerializer):
    answersCount = serializers.SerializerMethodField()

    class Meta:
        model = AdQuestion
        fields = ['id', 'question_text', 'answersCount']  # Убедитесь, что используете правильное имя поля

    def get_answersCount(self, obj):
        return obj.answers.count()


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ['id', 'name']


class BoostSerializer(serializers.Serializer):
    isBoost = serializers.BooleanField(default=False)
    multiplier = serializers.IntegerField(default=0)
    boostEndDate = serializers.DateTimeField(allow_null=True)


class AdSerializerWithCompany(serializers.ModelSerializer):
    company = CompanySerializer()
    boost = BoostSerializer(allow_null=True)  # Указываем, что boost может быть null

    class Meta:
        model = BaseAd
        fields = ['id', 'created_at', 'title', 'ad_type', 'description', 'company', 'boost']


class GetAdsResponseSerializer(serializers.Serializer):
    data = AdSerializerWithCompany(many=True)