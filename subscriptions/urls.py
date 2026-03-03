from django.urls import path

from . import views

urlpatterns = [
    path("<slug:user_id>", views.subscribe),
    path("me/", views.get_status),  # GET, DELETE
]
