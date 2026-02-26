from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.TextField(
        verbose_name="Название",  # не "Содержание" для категории
        max_length=200,
        unique=True,
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="URL-идентификатор",
        help_text="Будет создан автоматически из названия",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Автоматическое создание slug, если его нет
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
