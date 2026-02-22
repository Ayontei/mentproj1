from django.contrib import admin
from django.urls import path, include
import users.urls
import posts.urls
import categories.urls
import tags.urls
import subscriptions.urls
from posts.views import page_not_found


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('auth/', include(users.urls)),
    path('posts/', include(posts.urls)),
    path('categories/',include(categories.urls)),
    path('tags/', include(tags.urls)),
    path('subscriptions', include(subscriptions.urls)),
]

handler404 = page_not_found
