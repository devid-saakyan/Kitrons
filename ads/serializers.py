from rest_framework import serializers
from .models import *


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
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