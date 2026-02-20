from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    """
    Статьи, принадлежащие пользователям
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # Кто создал - берем из JWT токена
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles'  # user.articles.all()
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"