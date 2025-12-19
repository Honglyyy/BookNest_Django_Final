from django.http import request

from .models import Category, Genre

def fiction_genres(request):
    DTFictionGenre = Genre.objects.filter(categoryId = 1)
    return {
        'DTFictionGenre': DTFictionGenre,
    }

def non_fiction_genres(request):
    DTNonFictionGenre = Genre.objects.filter(categoryId = 2)
    return {
            'DTNonFictionGenre': DTNonFictionGenre,
    }

def technology_genres(request):
    DTTechnologyGenre = Genre.objects.filter(categoryId = 3)
    return {
        'DTTechnologyGenre': DTTechnologyGenre,
    }
