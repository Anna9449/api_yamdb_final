
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

from django.contrib.auth import get_user_model
from django.db import models

LENGTH_TEXT_OUTPUT = 30

User = get_user_model()


class Review(models.Model):
    text = models.TextField('Текст отзыва')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews'
    )
    author = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
        related_name='reviews'
    )
    score = models.PositiveIntegerField(
        'Оценка',
        default=10,
        help_text=('Поставьте оценку от 1 до 10.'))
    pub_date = models.DateTimeField(
        'Дата отзывы',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:LENGTH_TEXT_OUTPUT]


class Rating(models.Model):
    pass


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        'Дата комментария',
        auto_now_add=True
    )

    class Meta():
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:LENGTH_TEXT_OUTPUT]

