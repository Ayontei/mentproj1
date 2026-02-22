from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView  # Опционально: для проверки валидности токена
)

urlpatterns = [
    path('register/', views.user_reg, name='reg'),
    path('jwt/create', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/',views.cab, name='cabinet')
]
