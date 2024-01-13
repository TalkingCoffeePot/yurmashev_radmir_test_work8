from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Products(models.Model):
    CATEGORY = (
        ('s', 'Смартфон'),
        ('l', 'Ноутбук'),
        ('g', 'Видеокарта')
    )
    title = models.CharField('Название', max_length=100)
    category = models.CharField('Категория', max_length=1, choices=CATEGORY)
    description = models.TextField('Описание', max_length=100)
    image = models.ImageField('Картинка', uploads_to='media')


class Review(models.Model):
    RATING = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )
    author = models.ForeignKey(User, verbose_name='Автор', related_name='a_review')
    product = models.ForeignKey(Products, verbose_name='Продукт', related_name='p_review')
    text = models.TextField('Текст отзыва', max_length=1500)
    rate = models.IntegerField('Оценка', choices=RATING)
    moderate = models.BooleanField('Модерация', default=False)
    date_add = models.DateField('Дата публикации', auto_now_add=True)
    date_edit = models.DateField('Дата редактирования', auto_now=True)

