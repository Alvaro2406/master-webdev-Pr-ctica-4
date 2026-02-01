from rest_framework import viewsets
from .models import Producto
from .serializers import ProductoSerializer
from api_view_login.authentication import CookieJWTAuthentication
from utils.user_validation import HasJWTUser
from .permission import CanUseProducts

# Create your views here.
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    lookup_field = 'id_producto'
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [HasJWTUser, CanUseProducts]