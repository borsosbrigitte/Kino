from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Film)
admin.site.register(FilmRating)
admin.site.register(UserList)
admin.site.register(FilmList)