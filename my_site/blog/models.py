import email
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django.urls import reverse
from taggit.managers import TaggableManager

class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class Post(models.Model):
    tags = TaggableManager()
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликовано')
    )
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    slug = models.SlugField(max_length=250, unique_for_date='publish', verbose_name="СЛАГ")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name="Автор")
    body = models.TextField(verbose_name="Текст")

    publish = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Статус")
    
    objects = models.Manager() # Обычные или все статьи
    published = PublishManager()  # Только опубликованные статьи

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day,
                                                        self.slug])

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="пост")
    name = models.CharField(max_length=80, verbose_name="Имя")
    email = models.EmailField()
    body = models.TextField(verbose_name="Комментарий")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Комментирует {} статью {}'.format(self.name, self.post)



    