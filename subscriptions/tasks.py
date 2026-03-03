from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Sub
import logging

logger = logging.getLogger(__name__)


@shared_task
def notify_subscribers(author_id, post_title, post_id):
    """
    Отправляет уведомления всем подписчикам автора о новом посте
    """
    try:
        author = User.objects.get(id=author_id)
        subscribers = Sub.objects.filter(
            target_user=author, is_active=True
        ).select_related("subscriber")

        subscriber_emails = [
            sub.subscriber.email for sub in subscribers if sub.subscriber.email
        ]

        if not subscriber_emails:
            logger.info(f"No subscribers with email for user {author.username}")
            return f"No subscribers to notify for post {post_id}"

        # Отправка email
        send_mail(
            subject=f"Новый пост от {author.username}",
            message=(
                f'Пользователь {author.username} опубликовал новый пост: "{post_title}"\n\n'
                f"Ссылка: http://127.0.0.1/posts/{post_id}/"
            ),
            from_email="noreply@your-site.com",
            recipient_list=subscriber_emails,
            fail_silently=False,
        )

        logger.info(
            f"Notified {len(subscriber_emails)} subscribers about post {post_id}"
        )
        return f"Notified {len(subscriber_emails)} subscribers"

    except User.DoesNotExist:
        logger.error(f"User {author_id} not found")
        return f"User {author_id} not found"
    except Exception as e:
        logger.error(f"Error notifying subscribers: {e}")
        raise
