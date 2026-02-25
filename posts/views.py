from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from subscriptions.tasks import notify_subscribers

from .models import Post  # ваша модель
from .serializers import PostSerializer


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


@api_view(["GET", "POST"])
def post_list(request):
    if request.method == "GET":
        # Базовый queryset (только опубликованные посты)
        posts = Post.objects.filter(is_published=True)

        # 🔍 ПОИСК по title и content
        search = request.GET.get("search")
        if search:
            posts = posts.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )

        # 🏷️ ФИЛЬТРАЦИЯ по категории
        category_id = request.GET.get("category")
        if category_id:
            posts = posts.filter(categories_id=category_id)

        # 🏷️ ФИЛЬТРАЦИЯ по тегу
        tag_id = request.GET.get("tag")
        if tag_id:
            posts = posts.filter(tags__id=tag_id)

        # 👤 ФИЛЬТРАЦИЯ по автору
        author_id = request.GET.get("author")
        if author_id:
            posts = posts.filter(author_id=author_id)

        # 📅 ФИЛЬТРАЦИЯ по датам
        created_after = request.GET.get("created_after")
        if created_after:
            posts = posts.filter(created_at__gte=created_after)

        created_before = request.GET.get("created_before")
        if created_before:
            posts = posts.filter(created_at__lte=created_before)

        # 🔄 СОРТИРОВКА
        ordering = request.GET.get(
            "ordering", "-created_at"
        )  # по умолчанию новые сверху
        # Проверяем разрешенные поля для сортировки
        allowed_ordering = ["created_at", "-created_at", "title", "-title"]
        if ordering in allowed_ordering:
            posts = posts.order_by(ordering)
        else:
            posts = posts.order_by("-created_at")

        # 📄 ПАГИНАЦИЯ
        paginator = PostPagination()
        paginated_posts = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(paginated_posts, many=True)

        # Возвращаем пагинированный ответ с метаданными
        return paginator.get_paginated_response(
            {
                "posts": serializer.data,
                "total": paginator.page.paginator.count,
                "page": paginator.page.number,
                "page_size": paginator.page_size,
            }
        )

    elif request.method == "POST":
        # Проверка авторизации
        if not request.user.is_authenticated:
            return Response(
                {"error": "Только для авторизованных пользователей"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            # Сохраняем пост и получаем объект
            post = serializer.save(author=request.user)

            # Асинхронно уведомляем подписчиков (только для опубликованных постов)
            if post.is_published:
                notify_subscribers.delay(
                    author_id=request.user.id, post_title=post.title, post_id=post.id
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def get_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)  # получаем тег один раз для всех методов
    except Post.DoesNotExist:
        return Response({"Err": "Пост не найден"}, status=404)

    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)

    if not (request.user.is_staff or request.user == post.author):
        return Response({"error": "Недостаточно прав"}, status=403)

    if request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == "PATCH":
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == "DELETE":
        post.delete()
        return Response({"message": f"Пост {post_id} удален"}, status=204)


def page_not_found(request, exception):
    return Response({"Err": "Страница не найдена"})
