from django.urls import path
from . import views
from .views import ShowAllActors, ShowDirectorInfo, ShowActorInfo


urlpatterns = [
    path('', views.show_all_movie),
    path('directors', views.show_all_directors),
    path('directors/<slug:slug_director>', ShowDirectorInfo.as_view(), name="director_info"),
    path('actors/', ShowAllActors.as_view()),
    path('actors/<slug:slug_actor>', ShowActorInfo.as_view(), name="actor_info"),
    path('movie/<slug:slug_movie>', views.show_one_movie, name="movie_info"),
]
