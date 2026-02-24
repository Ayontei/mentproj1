from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """
    Генерирует access и refresh токены для пользователя
    """
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api_view(["POST"])
@permission_classes([AllowAny])
def user_reg(request):
    """
    Регистрация нового пользователя с немедленной выдачей токенов
    POST: username, password, email (опционально)
    """
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email", "")

    # Валидация
    if not username or not password:
        return Response(
            {"error": "Необходимо указать username и password"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Проверка существования пользователя
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Пользователь с таким именем уже существует"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Создание пользователя
    user = User.objects.create_user(username=username, password=password, email=email)

    # Генерация токенов
    tokens = get_tokens_for_user(user)

    return Response(
        {
            "message": "Регистрация успешна",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "tokens": tokens,  # access и refresh токены
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cab(request):
    user = request.user

    return Response(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "date_joined": user.date_joined,
        }
    )
