from django.contrib import admin
from django.urls import path, include
import users.urls
import posts.urls
from posts.views import page_not_found


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('auth/', include(users.urls)),
    path('posts/', include(posts.urls)),
]

handler404 = page_not_found
