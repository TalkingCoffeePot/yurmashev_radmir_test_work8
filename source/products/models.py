from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

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
    image = models.ImageField('Картинка', upload_to='products')

    def get_avg_rate(self):
        this_reviews = self.p_review.filter(moderate=True)
        avg_sum = this_reviews.aggregate(Avg('rate'))
        return avg_sum['rate__avg']


class Review(models.Model):
    RATING = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )
    author = models.ForeignKey(User, verbose_name='Автор', related_name='a_review', on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Products, verbose_name='Продукт', related_name='p_review', on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField('Текст отзыва', max_length=1500)
    rate = models.IntegerField('Оценка', choices=RATING, blank=False, default=1)
    moderate = models.BooleanField('Модерация', default=False)
    date_add = models.DateField('Дата публикации', auto_now_add=True)
    date_edit = models.DateField('Дата редактирования', auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_author(self):
        return User.objects.get(username=self.author)
    
    def get_product(self):
        return Products.objects.get(id=self.product)

