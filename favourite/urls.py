from django.urls import path
from .views import MakeFavouriteView, RemoveFavouriteView, GetUserFavouritesView

urlpatterns = [
    path('MakeFavourite/<int:id>/', MakeFavouriteView.as_view(), name='make_favourite'),
    path('RemoveFavourite/<int:id>/', RemoveFavouriteView.as_view(), name='remove_favourite'),
    path('GetUserFavourites/', GetUserFavouritesView.as_view(), name='get_user_favourites'),
]
