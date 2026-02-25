from celery import shared_task
from django.contrib.auth.models import User

from .models import Sub


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

        # if not subscriber_emails:
        #     print(f"No subscribers with email for user {author.username}")
        #     return f"No subscribers to notify for post {post_id}"

        # Отправка email (можно заменить на другой канал)
        print(
            subject=f"Новый пост от {author.username}",
            message=(
                f'Пользователь {author.username}a\
                опубликовал новый пост: "{post_title}"\n\n'
                f"Ссылка: http: //127.0.0.1/posts/{post_id}/"
            ),
            from_email="noreply@your-site.com",
            recipient_list=subscriber_emails,
            fail_silently=False,
        )

        print(f"Notified {len(subscriber_emails)} subscribers about post {post_id}")
        return f"Notified {len(subscriber_emails)} subscribers"

    except User.DoesNotExist:
        print(f"User {author_id} not found")
        return f"User {author_id} not found"
    except Exception as e:
        print(f"Error notifying subscribers: {e}")
