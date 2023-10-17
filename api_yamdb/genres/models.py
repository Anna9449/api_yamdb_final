from django.db import models


class Genres(models.Model):
    name = models.TextField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(max_length=50, unique=True,
                            verbose_name='Слаг жанра')
