from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from .models import Film, UserList, FilmList

urlpatterns = [
    path('', views.index, name='index'),
    path('film/<int:pk>', views.FilmDetailView.as_view(model=Film), name='film_detail'),
    path('watchlists/', login_required(views.UserListsView.as_view(model=UserList)), name='watchlists'),
    path('watchlists/<int:pk>', views.watch_list_view, name='watchlist'),
    path('watchlists/<int:pk>/delete/', views.delete_watchlist_view, name='delete_watchlist'),
    path('watchlists/<int:pk>/edit/', views.edit_watchlist_name_view, name='edit_watchlist_name'),
    path('watchlists/<int:wpk>/delete_film/<int:fpk>', views.delete_watchlist_film, name='delete_watchlist_film'),
    path('film/<int:fpk>/add_film_to_watchlist/', views.add_film_to_watchlist, name='add_film_to_watchlist'),
    path('film/<int:fpk>/rate_film/', views.rate_film, name='rate_film'),
]
