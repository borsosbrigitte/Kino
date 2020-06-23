from django.shortcuts import render

# Create your views here.
from .models import Film, FilmList, FilmRating, UserList, User


def index(request):
    films = Film.objects.all()

    context = {
        'films': films
    }

    return render(request, 'index.html', context=context)