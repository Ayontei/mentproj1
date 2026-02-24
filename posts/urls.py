from django.urls import path

from . import views

urlpatterns = [
    path("", views.post_list),  # GET, POST
    path("<slug:post_id>/", views.get_post),  # GET, PATCH, PUT, DELETE
]
