from rest_framework import serializers

from .models import Category  # импортируем модель Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "created_at"]
        read_only_fields = ["id", "created_at"]  # эти поля нельзя менять через API
