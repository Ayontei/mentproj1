from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

import categories.urls
import posts.urls
import subscriptions.urls
import tags.urls
import users.urls
from posts.views import page_not_found

schema_view = get_schema_view(
    openapi.Info(
        title="MentProj API",
        default_version="v1",
        description="Документация API для проекта MentProj",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="steameprofile@mail.ru"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],  # Разрешить доступ к документации всем
)

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("auth/", include(users.urls)),
    path("posts/", include(posts.urls)),
    path("categories/", include(categories.urls)),
    path("tags/", include(tags.urls)),
    path("subscriptions", include(subscriptions.urls)),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

handler404 = page_not_found
