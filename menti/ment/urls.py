"""
URL configuration for ment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import users.urls
import posts.urls
from posts.views import page_not_found


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('user/', include(users.urls)),
    path('', include(posts.urls)),
]

handler404 = page_not_found

'''Сегодня реализовал JWT авторизацию, прописал пути для генерации  acsess и refresh токенов так же правильную их выдачу при регистрации и авторизации
Разобрался с системой ролей и доступами к API'''