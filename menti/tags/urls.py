from django.urls import path
from . import views

urlpatterns = [
    path('', views.tags_list), # GET, POST
    path('<slug:id>/', views.get_tag), # GET, PATCH, PUT, DELETE
]
