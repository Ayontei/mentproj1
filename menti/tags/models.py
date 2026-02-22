from django.db import models
from django.utils.text import slugify

class Tags(models.Model):
    name = models.TextField(
        verbose_name="Содержание",
        max_length=200,
        unique=True,
    ),
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="URL-идентификатор",
        help_text="Будет создан автоматически из заголовка"
    ),

    def save(self, *args, **kwargs):
        # Автоматическое создание slug, если его нет
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)