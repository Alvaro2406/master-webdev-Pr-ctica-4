from django.contrib import admin
from django.urls import path, include
"""
URL configuration for just_globo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # path('admin/', admin.site.urls),ç
    path('role/', include('api_view_roles.urls')),
    path('user/', include('viewset_usuarios.urls')),
    path('establecimiento/', include('api_view_establecimiento.urls')),
    path('producto/', include('viewset_productos.urls')),
    path('pedido/', include('api_view_pedidos.urls')),
    path('auth/', include('api_view_login.urls')),
]
