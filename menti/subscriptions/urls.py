from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscribe),
    path('me/', views.get_status), # GET, DELETE
]
