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
    page_size = 10  # Значение по умолчанию

    def get_page_size(self, request):
        # Получаем значение `count` из данных запроса
        page_size = request.data.get('count') or request.query_params.get('count')
        if page_size:
            try:
                return int(page_size)
            except ValueError:
                pass
        return self.page_size

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
    pagination_class = CustomPageNumberPagination
    serializer_class = AdSerializerWithCompany

    @swagger_auto_schema(
        operation_description="Получение списка объявлений с пагинацией",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'page': openapi.Schema(type=openapi.TYPE_INTEGER, description='Номер страницы', default=1),
                'count': openapi.Schema(type=openapi.TYPE_INTEGER, description='Количество элементов на странице',
                                        default=10),
            },
            required=['page', 'count']
        ),
        responses={200: AdSerializerWithCompany(many=True)}
    )
    def post(self, request, *args, **kwargs):
        page_number = request.data.get('page', 1)
        count = request.data.get('count', 10)
        paginator = self.pagination_class()
        paginator.page_size = count
        queryset = BaseAd.objects.all().order_by('-created_at')
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


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
