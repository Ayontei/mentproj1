from rest_framework import serializers

from .models import Tags  # импортируем модель Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ["id", "name", "slug", "created_at"]
        read_only_fields = ["id", "created_at"]  # эти поля нельзя менять через API
