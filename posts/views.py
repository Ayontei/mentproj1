from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post  # ваша модель
from .serializers import PostSerializer


@api_view(["GET", "POST"])
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.values_list("title", flat=True)
        # serializer = PostSerializer(posts, many=True)
        return Response(list(posts))
    elif request.method == "POST":
        if not request.user.is_authenticated:  # или is_superuser
            return Response(
                {"error": "Только для авторизованных пользователей"}, status=403
            )
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # ← ЗДЕСЬ вызывается save()
            return Response(serializer.data, status=201)


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
