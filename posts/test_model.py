import pytest
from model_bakery import baker

from posts.models import Post


@pytest.mark.django_db  # разрешаем доступ к базе данных
def test_post_creation():
    """Тест создания поста"""
    post = baker.make(Post, title="Test Post", content="Test Content")

    assert post.title == "Test Post"
    assert post.content == "Test Content"
    assert post.slug is not None  # slug должен создаться автоматически
    assert str(post) == "Test Post"  # проверка __str__ метода
