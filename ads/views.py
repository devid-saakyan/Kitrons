from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response
from .models import BaseAd
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'success': True,
            'data': {
                'data': data,
                'pageCount': self.page.paginator.num_pages,
                'itemCount': self.page.paginator.count,
            },
            'messages': []
        })


class GetAdsView(generics.ListAPIView):
    queryset = BaseAd.objects.all()
    serializer_class = AdSerializerWithCompany
    pagination_class = CustomPageNumberPagination

    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter('page', openapi.IN_QUERY, description="A page number within the paginated result set.",
    #                           type=openapi.TYPE_INTEGER),
    #         openapi.Parameter('page_size', openapi.IN_QUERY, description="Number of items per page.",
    #                           type=openapi.TYPE_INTEGER),
    #     ]
    # )
    # def get(self, request, *args, **kwargs):
    #     page = self.paginate_queryset(self.get_queryset())
    #     serializer = self.get_serializer(page, many=True) if page is not None else self.get_serializer(
    #         self.get_queryset(), many=True)
    #     response_data = {
    #         'success': True,
    #         'data': {
    #             'data': serializer.data,
    #             'pageCount': self.paginator.page.paginator.num_pages if page is not None else 1,
    #             'itemCount': self.paginator.page.paginator.count if page is not None else len(serializer.data),
    #         },
    #         'messages': []
    #     }
    #     return self.get_paginated_response(response_data) if page is not None else Response(response_data)


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
                    'data': [serializer.data]
                }
            })
        except BaseAd.DoesNotExist:
            return Response({'success': False, 'message': 'Ad not found.'}, status=404)


class GetAdsByCompanyIdView(generics.ListAPIView):
    serializer_class = AdSerializerWithCompany
    pagination_class = PageNumberPagination

    def get_queryset(self):
        company_id = self.kwargs.get('companyId')
        return BaseAd.objects.filter(company_id=company_id)

    def get(self, request, *args, **kwargs):
        ads = self.get_queryset()
        serializer = AdSerializerWithCompany(ads, many=True)
        return self.get_paginated_response({
            'success': True,
            'data': serializer.data
        })


class GetAdsQuestionView(generics.ListAPIView):
    serializer_class = AdQuestionResponseSerializer
    pagination_class = PageNumberPagination

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
    pagination_class = PageNumberPagination
    def get_queryset(self):
        return UserAdHistory.objects.filter(user=self.request.user)
