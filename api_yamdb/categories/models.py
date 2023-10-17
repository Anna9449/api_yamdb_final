from django.db import models


class Categories(models.Model):
    name = models.TextField(max_length=256, verbose_name='Названик категории')
    slug = models.SlugField(max_length=50, unique=True,
                            verbose_name='Слаг категории')
