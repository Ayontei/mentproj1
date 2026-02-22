from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,
         on_delete=models.CASCADE,
        related_name='profile'
)
    subscriber = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL,  # или CASCADE
        null=True, 
        blank=True,
        unique=True,  # Это гарантирует, что на одного юзера может подписаться только один
        related_name='subscribed_to_me'  # кто подписан на меня
)
    subscribed_to = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True, 
        unique=True,  # Это гарантирует, что юзер подписан только на одного
        related_name='my_subscriber'  # на кого я подписан
)