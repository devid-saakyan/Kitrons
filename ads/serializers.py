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
        fields = '__all__'


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
        fields = '__all__'


class BoostSerializer(serializers.Serializer):
    isBoost = serializers.BooleanField(default=False)
    multiplier = serializers.IntegerField(default=0)
    boostEndDate = serializers.DateTimeField(allow_null=True)


class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['image']


class AdSerializerWithCompany(serializers.ModelSerializer):
    company = CompanySerializer()
    boost = BoostSerializer(allow_null=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = BaseAd
        fields = '__all__'

    def get_images(self, obj):
        return [image.image.url for image in obj.images.all()]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        ad_type_mapping = {
            'survey': 1,
            'video': 2,
            'post': 3
        }
        representation['adsType'] = ad_type_mapping.get(instance.ad_type, None)
        representation.pop('ad_type', None)
        return representation