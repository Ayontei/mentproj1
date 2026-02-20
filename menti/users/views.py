from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

def get_tokens_for_user(user):
    """
    Генерирует access и refresh токены для пользователя
    """
    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
@permission_classes([AllowAny])
def user_reg(request):
    """
    Регистрация нового пользователя с немедленной выдачей токенов
    POST: username, password, email (опционально)
    """
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    # Валидация
    if not username or not password:
        return Response(
            {'error': 'Необходимо указать username и password'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Проверка существования пользователя
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Пользователь с таким именем уже существует'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Создание пользователя
    user = User.objects.create_user(
        username=username, 
        password=password, 
        email=email
    )
    
    # Генерация токенов
    tokens = get_tokens_for_user(user)
    
    return Response({
        'message': 'Регистрация успешна',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
        'tokens': tokens  # access и refresh токены
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_auth(request):
    """
    Авторизация пользователя с выдачей токенов
    POST: username, password
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Валидация
    if not username or not password:
        return Response(
            {'error': 'Необходимо указать username и password'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Аутентификация
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Генерация токенов
        tokens = get_tokens_for_user(user)
        
        return Response({
            'message': 'Авторизация успешна',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'tokens': tokens  # access и refresh токены
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Неверное имя пользователя или пароль'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def token_refresh(request):
    """
    Обновление access токена по refresh токену
    POST: refresh (refresh token)
    """
    refresh_token = request.data.get('refresh')
    
    if not refresh_token:
        return Response(
            {'error': 'Необходимо указать refresh токен'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        
        # Если включена ротация refresh токенов
        if getattr(settings, 'SIMPLE_JWT', {}).get('ROTATE_REFRESH_TOKENS', False):
            new_refresh_token = str(refresh)
            return Response({
                'access': access_token,
                'refresh': new_refresh_token
            })
        else:
            return Response({
                'access': access_token
            })
            
    except Exception as e:
        return Response(
            {'error': 'Недействительный refresh токен'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Выход из системы (помещает refresh токен в черный список)
    POST: refresh (refresh token)
    """
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Необходимо указать refresh токен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        token = RefreshToken(refresh_token)
        token.blacklist()  # Добавляем в черный список
        
        return Response({
            'message': 'Выход выполнен успешно'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': 'Недействительный refresh токен'}, 
            status=status.HTTP_400_BAD_REQUEST
        )



def user_reg(request):
    return HttpResponse('Reg page')
    
def user_auth(request):
    return HttpResponse('Auth page')
