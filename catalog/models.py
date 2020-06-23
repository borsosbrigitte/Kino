from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Film(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    poster = models.CharField(max_length=500)

    def __str__(self):
        return self.title


class FilmRating(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    film_id = models.ForeignKey(Film, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])

    def __str__(self):
        return str(self.user_id) + "," + str(self.film_id) + "," + str(self.rating)


class UserList(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_id) + "'s list " + str(self.pk)


class FilmList(models.Model):
    list_id = models.ForeignKey(UserList, on_delete=models.CASCADE)
    film_id = models.ForeignKey(Film, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.list_id) + "," + str(self.film_id)

