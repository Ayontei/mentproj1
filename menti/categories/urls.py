from django.urls import path
from . import views

urlpatterns = [
    path('', views.categoriest_list), # GET, POST
    path('<slug:id>/', views.get_category),
    path('<int:id>',views.change_category), # PUT,PATCH,DELETE
]
