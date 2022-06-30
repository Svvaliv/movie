from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    director_email = models.EmailField()
    slug = models.SlugField(default="", null=False, db_index=True)

    def get_url(self):
        return reverse("director_info", args=[self.slug])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DressingRoom(models.Model):
    floor = models.IntegerField()
    room = models.IntegerField()

    def __str__(self):
        return f"Этаж {self.floor}, комната {self.room}"



class Actor(models.Model):
    MALE = "M"
    FEMALE = "F"
    GENDERS = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDERS, default="")
    dressing = models.OneToOneField(DressingRoom, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(default="", null=False, db_index=True)

    def get_url(self):
        return reverse("actor_info", args=[self.slug])

    def __str__(self):
        if self.gender == self.MALE:
            return f"Actor - {self.first_name} {self.last_name}"
        return f"Actress - {self.first_name} {self.last_name}"


class Movie(models.Model):
    EUR = "EUR"
    USD = "USD"
    RUB = "RUB"
    CURRENCY_CHOICES = [
        (EUR, 'Euro'),
        (USD, 'Dollar'),
        (RUB, 'Rubles'),
    ]
    name = models.CharField(max_length=40)
    rating = models.IntegerField(validators=[MinValueValidator(1),
                                             MaxValueValidator(100)])
    year = models.IntegerField(null=True, blank=True)
    budget = models.IntegerField(default=1_000_000,
                                 validators=[MinValueValidator(1)])
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=RUB)
    slug = models.SlugField(default="", null=False, db_index=True)
    director = models.ForeignKey(Director, on_delete=models.PROTECT, null=True)
    actors = models.ManyToManyField(Actor)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Movie, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("movie_info", args=[self.slug])

    def __str__(self):
        return f"{self.name} - {self.rating}%"


#  python3 manage.py shell_plus --print-sql