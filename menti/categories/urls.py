from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list), # GET, POST
    path('<slug:id>/', views.get_category), # GET,PUT,PATCH,DELETE
]
