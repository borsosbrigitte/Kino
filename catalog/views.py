from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
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
        context = super(FilmDetailView, self).get_context_data(**kwargs)
        film_ratings = FilmRating.objects\
            .filter(user_id__exact=self.request.user.pk)\
            .filter(film_id__exact=self.object.pk)

        no_of_ratings = film_ratings.count()
        if no_of_ratings == 0:
            context['rating'] = 0
        else:
            context['rating'] = film_ratings.last().rating

        watchlists = UserList.objects.filter(user_id__exact=self.request.user.pk)
        context['watchlists'] = watchlists

        return context


class UserListsView(generic.ListView):
    model = UserList
    template_name = "catalog/watchlists.html"

    def get_queryset(self):
        return UserList.objects.filter(user_id__exact=self.request.user.pk)

    def post(self, request, **kwargs):
        watchlist_name = request.POST.get('name_field')
        watchlist = UserList(user_id=self.request.user, list_name=watchlist_name)
        watchlist.save()
        return HttpResponseRedirect('/watchlists/')


@login_required
def watch_list_view(request, pk):
    film_list_items = FilmList.objects.filter(list_id__exact=pk)
    film_pks = []
    for film in film_list_items:
        film_pks.append(film.film_id.pk)

    films = sorted(Film.objects.filter(pk__in=film_pks), key=lambda film: film.title)

    watchlist = UserList.objects.filter(pk__exact=pk).first()
    context = {
        'watchlist': watchlist,
        'films': films
    }

    return render(request, 'catalog/watchlist.html', context=context)


@login_required()
def delete_watchlist_view(request, pk):
    UserList.objects.filter(pk=pk).delete()
    return HttpResponseRedirect('/watchlists/')


@login_required()
def edit_watchlist_name_view(request, pk):
    if request.method == 'GET':
        watchlist = UserList.objects.filter(pk=pk).first()
        context = {
            'watchlist': watchlist
        }

        return render(request, 'catalog/edit_watchlist_name.html', context=context)
    elif request.method == 'POST':
        UserList.objects.filter(pk=pk).update(list_name=request.POST.get('name_field'))
        return HttpResponseRedirect('/watchlists/')


@login_required()
def delete_watchlist_film(request, wpk, fpk):
    FilmList.objects.filter(list_id=wpk).filter(film_id=fpk).delete()
    return HttpResponseRedirect('../../../watchlists/' + str(wpk))


@login_required()
def add_film_to_watchlist(request, fpk):
    wpk = int(request.POST['watchlist'])
    watchlist = UserList.objects.filter(pk=wpk).first()
    film = Film.objects.filter(pk=fpk).first()
    film_list = FilmList(list_id=watchlist, film_id=film)
    film_list.save()
    return HttpResponseRedirect('../../../watchlists/' + str(wpk))


@login_required()
def rate_film(request, fpk):
    film = Film.objects.filter(pk=fpk).first()

    rating = int(request.POST['rate'])

    if len(FilmRating.objects.filter(user_id__exact=request.user).filter(film_id__exact=film)) == 0:
        film_rating = FilmRating(user_id=request.user, film_id=film, rating=rating)
        film_rating.save()
    else:
        FilmRating.objects.filter(user_id__exact=request.user)\
            .filter(film_id__exact=film)\
            .update(rating=rating)

    return HttpResponseRedirect('../../../film/' + str(fpk))

