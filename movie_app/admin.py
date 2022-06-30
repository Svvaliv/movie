from django.contrib import admin, messages
from .models import Movie, Director, Actor, DressingRoom
from django.db.models import QuerySet


# Register your models here.
class RatingFilter(admin.SimpleListFilter):
    title = "rating"
    parameter_name = "rating"

    def lookups(self, request, model_admin):
        return [
            ("<40", "Low"),
            ("from 40 to 59", "Middle"),
            ("from 60 to 79", "High"),
            (">=80", "Very High"),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == "<40":
            return queryset.filter(rating__lt=40)
        elif self.value() == "from 40 to 59":
            return queryset.filter(rating__gte=40).filter(rating__lt=60)
        elif self.value() == "from 60 to 79":
            return queryset.filter(rating__gte=60).filter(rating__lt=80)
        elif self.value() == ">=80":
            return queryset.filter(rating__gte=80)


# admin.site.register(Director)
# admin.site.register(DressingRoom)

@admin.register(DressingRoom)
class DressingRoomAdmin(admin.ModelAdmin):
    ordering = ["floor", "room"]
    list_display = ['floor', 'room', 'actor']


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("first_name", "last_name")}
    ordering = ["first_name"]
    list_display = ['first_name', 'last_name', 'director_email']
    readonly_fields = ['director_email']


@admin.register(Actor)
class ActorsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("first_name", "last_name")}
    ordering = ["first_name"]
    list_display = ['first_name', 'last_name', 'gender']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    # fields = ['name', 'rating', 'currency']
    # exclude = ['slug']
    # readonly_fields = ['budget']
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'rating', 'director', 'budget', 'rating_status']
    list_editable = ['rating', 'director', 'budget']
    filter_horizontal = ["actors"]
    ordering = ['name']
    list_per_page = 10
    actions = ["set_dollars", "set_euro", "set_rubles"]
    search_fields = ['name__startswith', 'rating']
    list_filter = ['name', RatingFilter, 'currency']

    @admin.display(ordering="rating", description="Статус")
    def rating_status(self, movie: Movie):
        if movie.rating < 50:
            return "Зачем это смотреть"
        if movie.rating < 70:
            return "Разок можно глянуть"
        if movie.rating <= 85:
            return "Зачет"
        else:
            return "Топчик"

    @admin.action(description="Установить валюту в доллар")
    def set_dollars(self, request, qs: QuerySet):
        count_choices = qs.update(currency=Movie.USD)
        self.message_user(
            request,
            f"Было обновлено {count_choices} записей"
        )

    @admin.action(description="Установить валюту в евро")
    def set_euro(self, request, qs: QuerySet):
        count_choices = qs.update(currency=Movie.EUR)
        self.message_user(
            request,
            f"Было обновлено {count_choices} записей"
        )

    @admin.action(description="Установить валюту в рубли")
    def set_rubles(self, request, qs: QuerySet):
        count_choices = qs.update(currency=Movie.RUB)
        self.message_user(
            request,
            f"Было обновлено {count_choices} записей",
        )
