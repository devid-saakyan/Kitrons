from rest_framework import generics
from .models import Ad
from .serializers import AdSerializer


class AdListView(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdDetailView(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer