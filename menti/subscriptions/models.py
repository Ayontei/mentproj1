from django.db import models
from django.contrib.auth.models import User

class Sub(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='user'
    )
    is_active = models.BooleanField(

    )