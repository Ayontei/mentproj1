from rest_framework import serializers

from .models import Post  # импортируем модель Tag


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)
    categories_name = serializers.CharField(source="categories.name", read_only=True)
    tags_list = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "is_published",
            "slug",
            "tags",
            "author",
            "updated_at",
            "author_name",
            "created_at",
            "categories",
            "categories_name",
            "tags_list",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "author",
        ]  # эти поля нельзя менять через API
