from django.urls import path
from . import views
from .models import Film, UserList, FilmList

urlpatterns = [
    path('', views.index, name='index'),
    path('film/<int:pk>', views.FilmDetailView.as_view(model=Film), name='film_detail'),
    path('watchlists/', views.UserListsView.as_view(model=UserList), name='watchlists'),
    path('watchlists/<int:pk>', views.WatchListView.as_view(model=FilmList), name='watchlist'),
]
