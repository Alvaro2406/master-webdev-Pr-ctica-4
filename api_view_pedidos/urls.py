from .views import pedido_create, pedido_list, pedido_detail, pedido_update, pedido_delete
from django.urls import path

urlpatterns = [
    path('create/', pedido_create, name='pedido_create'),
    path('list/', pedido_list, name='pedido_list'),
    path('detail/<int:id_pedido>/', pedido_detail, name='pedido_detail'),
    path('update/<int:id_pedido>/', pedido_update, name='pedido_update'),
    path('delete/<int:id_pedido>/', pedido_delete, name='pedido_delete'),
]