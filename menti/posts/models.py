from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from categories.models import Category
from tags.models import Tags

class Post(models.Model):
    id = models.AutoField(primary_key=True)  # Автоматически создается Django, можно не указывать
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
        help_text="Максимум 200 символов"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="URL-идентификатор",
        help_text="Будет создан автоматически из заголовка"
    )
    content = models.TextField(
        verbose_name="Содержание"
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликовано",
        help_text="Отметьте, чтобы опубликовать пост"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles'  # user.articles.all()
    )
    categories = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category'
    )
    tags = models.ManyToManyField(
        Tags,
        related_name='tags'
    )

    class Meta:
        ordering = ['-created_at']  # Сортировка по умолчанию (новые сверху)
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Автоматическое создание slug, если его нет
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

