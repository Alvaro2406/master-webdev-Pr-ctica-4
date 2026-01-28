from .views import establecimiento_create, establecimiento_list, establecimiento_detail, establecimiento_update, establecimiento_delete
from django.urls import path

urlpatterns = [
    path('list/', establecimiento_list, name='establecimiento_list'),
    path('create/', establecimiento_create, name='establecimiento_create'),
    path('details/<int:id_establecimiento>/', establecimiento_detail, name='establecimiento_detail'),
    path('update/<int:id_establecimiento>/', establecimiento_update, name='establecimiento_update'),
    path('delete/<int:id_establecimiento>/', establecimiento_delete, name='establecimiento_delete'),
]