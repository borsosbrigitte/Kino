from django.shortcuts import render
from django.views import generic

# Create your views here.
from .models import Film, FilmList, FilmRating, UserList, User


def index(request):
    films = sorted(Film.objects.all(), key=lambda film: film.title)

    context = {
        'films': films
    }

    return render(request, 'index.html', context=context)


class FilmDetailView(generic.DetailView):
    model = Film

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(FilmDetailView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        user_id = User.objects.filter(username__exact="bri").first()
        film_ratings = FilmRating.objects\
            .filter(user_id__exact=user_id)\
            .filter(film_id__exact=self.object.pk)

        no_of_ratings = film_ratings.count()
        if no_of_ratings == 0:
            context['rating'] = 0
        else:
            context['rating'] = film_ratings.last().rating
        return context


class UserListsView(generic.ListView):
    model = UserList
    template_name = "catalog/watchlists.html"

    def get_queryset(self):
        user_id = User.objects.filter(username__exact="bri").first()
        return UserList.objects.filter(user_id__exact=user_id)


class WatchListView(generic.ListView):
    model = FilmList
    template_name = "catalog/watchlist.html"

    def get_queryset(self):
        user_id = User.objects.filter(username__exact="bri").first()
        print(user_id)
