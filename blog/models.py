from django.db import models
from django.urls import reverse
from django.utils import timezone

from users.models import User


class Category(models.Model):
    """Модель Категорий"""
    title = models.CharField('Название категории', max_length=50)
    slug = models.SlugField('Url', unique=True, max_length=50)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField('Название тега', max_length=50)
    slug = models.SlugField('Url', unique=True, max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']


class Post(models.Model):
    """Модель постов"""
    author = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        verbose_name='Автор',
        default='Аноним'
    )
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    mini_text = models.TextField('Мини текст для превью', max_length=350)
    photo = models.ImageField('Фото для превью', upload_to='photo/%Y/%m/%d/')
    slug = models.SlugField('Url', unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    content = models.TextField('Основной текст', max_length=100000000000)
    published_date = models.DateTimeField('Дата публикации', default=timezone.now, blank=True, null=True)
    is_published = models.BooleanField('Публиковать', default=True)
    views = models.PositiveIntegerField('Просмотры', default=0)

    def __str__(self):
        return self.title

    def get_tags(self):
        return self.tags.all()

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-published_date']


class Comment(models.Model):
    """Модель комментариев"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    content = models.TextField('Текст комментария', max_length=50000)
    published_date = models.DateTimeField('Дата публикации', auto_now_add=True, blank=True)
    is_published = models.BooleanField('Показывать?', default=True)

    def __str__(self):
        return f'Автор {self.user.get_full_name()} пост {self.post}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-published_date']
