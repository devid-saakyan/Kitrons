from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from .serializers import *
from rest_framework.response import Response


class GetNewsFeedView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsListSerializer

    def get(self, request, *args, **kwargs):
        news = self.get_queryset()
        serializer = self.serializer_class(news, many=True)
        return Response({'success': True,
                          'data': serializer.data})


class GetNewsFeedByIdView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsListSerializer

    def get(self, request, *args, **kwargs):
        NewsId = self.kwargs.get('pk')
        try:
            news = self.get_queryset().get(id=NewsId)
            serializer = self.serializer_class(news)
            return Response({'success': True,
                             'data': {
                                 'data': serializer.data}
                             })
        except News.DoesNotExist:
            return Response({'success': False, 'message': 'There is no news with id {}'.format(NewsId)})


class GetNewsFeedByCompanyId(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsListSerializer

    def get(self, request, *args, **kwargs):
        companyId = self.kwargs.get('companyId')
        try:
            news = self.get_queryset().get(id=companyId)
            serializer = self.serializer_class(news)
            return Response({'success': True,
                             'data': {
                                 'data': serializer.data}
                             })
        except News.DoesNotExist:
            return Response({'success': False, 'message': 'There is no news with company id {}'.format(companyId)})