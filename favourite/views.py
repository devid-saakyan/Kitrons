from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Favourite
from .serializers import FavouriteSerializer


class MakeFavouriteView(generics.CreateAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, ad_id, *args, **kwargs):
        serializer = self.get_serializer(data={'user': request.user.id, 'ad': id})
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'Ad added to favourites.'}, status=201)
        return Response(serializer.errors, status=400)


class RemoveFavouriteView(generics.DestroyAPIView):
    queryset = Favourite.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, ad_id, *args, **kwargs):
        try:
            favourite = Favourite.objects.get(user=request.user, ad_id=id)
            favourite.delete()
            return Response({'success': True, 'message': 'Ad removed from favourites.'}, status=204)
        except Favourite.DoesNotExist:
            return Response({'success': False, 'message': 'Favourite not found.'}, status=404)


class GetUserFavouritesView(generics.ListAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)
