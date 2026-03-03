from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Sub


@api_view(["POST"])
def subscribe(request, user_id):
    if not request.user.is_authenticated:
        return Response({"Err": "Вам нужно авторизоваться"}, status=401)

    if not User.objects.filter(id=user_id).exists():
        return Response({"Err": "Пользователь не найден"}, status=404)

    if request.user.id == user_id:
        return Response({"Err": "Нельзя подписаться на себя"}, status=400)

    Sub.objects.create(subscriber=request.user, target_user_id=user_id, is_active=True)
    return Response({"message": f"Вы подписались на: {user_id}"})


@api_view(["GET", "DELETE"])
def get_status(request, user_id):
    if not request.user.is_authenticated:
        return Response({"Err": "Вам нужно авторизоваться"}, status=401)

    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"Err": "Пользователь не найден"}, status=404)

    if request.method == "GET":
        subscriptions = Sub.objects.filter(
            subscriber=request.user,
            is_active=True,  # только активные
        ).values_list("target_user__username", flat=True)

        return Response(list(subscriptions))

    elif request.method == "DELETE":
        # Удаляем подписку (или ставим is_active=False)
        deleted = Sub.objects.filter(
            subscriber=request.user, target_user=target_user
        ).update(is_active=False)  # или .delete()

        if deleted[0] > 0:
            return Response({"message": f"Вы отписались от {target_user.username}"})
        else:
            return Response({"Err": "Вы не были подписаны"}, status=400)
