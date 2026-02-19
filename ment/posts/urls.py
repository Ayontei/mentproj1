from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:post_id>/', views.get_post)
]
