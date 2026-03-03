from django.urls import path

from . import views

urlpatterns = [
    path("", views.post_list, name="post-list"),  # GET, POST
    path(
        "<slug:post_id>/", views.get_post, name="post-details"
    ),  # GET, PATCH, PUT, DELETE
]
