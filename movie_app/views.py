from django.db.models import F, Max, Min, Count, Avg, Value
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

# Create your views here.
from .models import Movie, Director, Actor


def show_all_directors(request):
    directors = sorted(Director.objects.all(), key=lambda director: director.first_name)
    return render(request, "movie_app/all_directors.html", context={
        "directors": directors,
    })


class ShowDirectorInfo(DetailView):
    template_name = "movie_app/director_info.html"
    model = Director
    slug_url_kwarg = 'slug_director'


# def show_director_info(request, slug_director: str):
#     director = get_object_or_404(Director, slug=slug_director)
#     return render(request, "movie_app/director_info.html", context={
#         "director": director,
#     })


class ShowAllActors(ListView):
    template_name = "movie_app/all_actors.html"
    model = Actor
    context_object_name = "actors"


class ShowActorInfo(DetailView):
    template_name = "movie_app/actor_info.html"
    model = Actor
    slug_url_kwarg = 'slug_actor'


# def show_actor_info(request, slug_actor: str):
#     actor = get_object_or_404(Actor, slug=slug_actor)
#     return render(request, "movie_app/actor_info.html", context={
#         "actor": actor,
#     })


def show_all_movie(request):
    # movies = Movie.objects.order_by(F("year").asc(nulls_last=True))
    movies = Movie.objects.annotate(
        true_bool=Value(True),
        false_bool=Value(False),
        new_budget=F("budget") * 1.5,
        rating_year=F("rating") * F("year"),
    )
    agg = movies.aggregate(Avg("budget"), Max("rating"), Min("rating"), Count("id"))
    for movie in movies:
        movie.save()
    return render(request, "movie_app/all_movies.html", {
        "movies": movies,
        "agg": agg,
    })


def show_one_movie(request, slug_movie: str):
    movie = get_object_or_404(Movie, slug=slug_movie)
    return render(request, "movie_app/one_movie.html", {
        "movie": movie,
    })
