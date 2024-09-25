from rest_framework import generics
from rest_framework.response import Response
from .models import BaseAd
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class GetAdsView(generics.ListAPIView):
    queryset = BaseAd.objects.all()

    def get(self, request, *args, **kwargs):
        ads = self.get_queryset()
        serializer = GetAdsResponseSerializer({'data': ads})
        return Response({
            'success': True,
            'data': serializer.data
        })


class GetAdsByIdView(generics.RetrieveAPIView):
    queryset = BaseAd.objects.all()

    def get(self, request, *args, **kwargs):
        ad_id = self.kwargs.get('pk')
        try:
            ad = self.get_queryset().get(id=ad_id)
            serializer = AdSerializerWithCompany(ad)
            return Response({
                'success': True,
                'data': {
                    'data': [serializer.data]  # Оборачиваем в 'data' для соответствия формату
                }
            })
        except BaseAd.DoesNotExist:
            return Response({'success': False, 'message': 'Ad not found.'}, status=404)


class GetAdsByCompanyIdView(generics.ListAPIView):
    serializer_class = AdSerializerWithCompany

    def get_queryset(self):
        company_id = self.kwargs.get('companyId')
        return BaseAd.objects.filter(company_id=company_id)

    def get(self, request, *args, **kwargs):
        ads = self.get_queryset()
        serializer = AdSerializerWithCompany(ads, many=True)
        return Response({
            'success': True,
            'data': {
                'data': [serializer.data]
            }
        })


class GetAdsQuestionView(generics.ListAPIView):
    serializer_class = AdQuestionResponseSerializer

    def get_queryset(self):
        ad_id = self.kwargs['AdId']
        return AdQuestion.objects.filter(ad_id=ad_id)


class ApplyAnswerView(generics.CreateAPIView):
    serializer_class = ApplyAnswerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            answer_id = serializer.validated_data['answerId']
            question_id = serializer.validated_data['questionId']
            ads_id = serializer.validated_data['adsId']

            try:
                question = AdQuestion.objects.get(id=question_id)
                print(question)
                correct_answer = question.correct_answer
                print(correct_answer)
                is_correct = (answer_id == correct_answer.id)

                UserAdHistory.objects.create(
                    user=request.user,
                    ad_id=ads_id,
                    action_type='answer',
                    is_correct=is_correct
                )

                return Response({"correct": is_correct}, status=status.HTTP_200_OK)
            except AdQuestion.DoesNotExist:
                return Response({"detail": "Question not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAdsHistoryView(generics.ListAPIView):
    serializer_class = UserAdHistorySerializer

    def get_queryset(self):
        # Возвращает историю действий для текущего пользователя
        return UserAdHistory.objects.filter(user=self.request.user)
