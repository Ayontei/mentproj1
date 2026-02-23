from django.urls import path
from . import views

urlpatterns = [
    path('', views.tags_list), # GET, POST
    path('<slug:tag_id>/', views.get_tag, name='Тэг'), # GET, PATCH, PUT, DELETE
]
