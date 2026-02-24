from django.db import models
from django.contrib.auth.models import User

class Sub(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions'  # на кого подписан я
    )
    target_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers'  # кто подписан на меня
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['subscriber', 'target_user']  # нельзя подписаться дважды
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subscriber.username} -> {self.target_user.username}"