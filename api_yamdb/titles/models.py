from django.db import models
from categories.models import Categories

from genres.models import Genres


class Titles(models.Model):
    name = models.TextField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(null=True)
    genre = models.ManyToManyField(Genres)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL,
                                 null=True, related_name='titles')
