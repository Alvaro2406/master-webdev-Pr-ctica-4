
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from utils.user_validation import HasJWTUser
from utils.user_role import check_admin_role
from django.http import JsonResponse
import json
from api_view_login.authentication import CookieJWTAuthentication
from .models import Pedido
from viewset_usuarios.models import User
from viewset_productos.models import Producto

# Create your views here.

@api_view(['POST'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([HasJWTUser])
def pedido_create(request):
    try: 
        json_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid Body'}, status=400)
    if 'id_usuario' not in json_data or 'productos' not in json_data:
        return JsonResponse({'error': 'Missing fields'}, status=400)
    usuario_id = json_data['id_usuario']
    try:
        usuario = User.objects.get(id_user=usuario_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuario not found'}, status=404)
    precio_total = 0
    pedido = Pedido.objects.create(
        usuario=usuario,
        precio_total=0
    )
    productos_data = json_data['productos']
    for producto_data in productos_data:
        try:
            producto = Producto.objects.get(id_producto=producto_data)
            pedido.productos.add(producto)
            precio_total += producto.precio
        except Producto.DoesNotExist:
            return JsonResponse({'error': f'Producto with id {producto_data} not found'}, status=404)
    pedido.precio_total = precio_total
    pedido.save()
    return JsonResponse(pedido.to_dict(), status=201)


@api_view(['GET'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([HasJWTUser])
def pedido_list(request):
    user = User.objects.get(username=request.user)
    if not check_admin_role(user):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    pedidos = Pedido.objects.all()
    pedidos_data = []
    for pedido in pedidos:
        productos = [] 
        for producto in pedido.productos.all():
            productos.append(producto)
        pedidos_data.append({
            'id_pedido': pedido.id_pedido,
            'fecha_pedido': pedido.fecha_pedido.isoformat(),
            'precio_total': str(pedido.precio_total),
            'id_usuario': pedido.usuario.id_user,
            'productos': [p.to_dict() for p in productos],

        })
        
    return JsonResponse(pedidos_data, safe=False)

@api_view(['GET'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([HasJWTUser])
def pedido_detail(request, id_pedido):
    try:
        pedido = Pedido.objects.get(id_pedido=id_pedido)
        user = User.objects.get(username=request.user)
        if not check_admin_role(user) or user.id_user != pedido.usuario.id_user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
    except Pedido.DoesNotExist:
        return JsonResponse({'error': 'Pedido not found'}, status=404)
    
    productos = [] 
    for producto in pedido.productos.all():
        productos.append(producto)
        
    pedido_data = {
        'id_pedido': pedido.id_pedido,
        'fecha_pedido': pedido.fecha_pedido.isoformat(),
        'precio_total': str(pedido.precio_total),
        'id_usuario': pedido.usuario.id_user,
        'productos': [p.to_dict() for p in productos],
    }
    
    return JsonResponse(pedido_data)


@api_view(['PUT'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([HasJWTUser])
def pedido_update(request, id_pedido):
    try: 
        json_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid Body'}, status=400)
    
    try:
        pedido = Pedido.objects.get(id_pedido=id_pedido)
        user = User.objects.get(username=request.user)
        if not check_admin_role(user) or user.id_user != pedido.usuario.id_user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
    except Pedido.DoesNotExist:
        return JsonResponse({'error': 'Pedido not found'}, status=404)
    
    if 'id_usuario' not in json_data or 'productos' not in json_data:
        return JsonResponse({'error': 'Missing fields'}, status=400)
    
    if 'productos' in json_data:
        pedido.productos.clear()
        precio_total = 0
        productos_data = json_data['productos']
        for producto_data in productos_data:
            try:
                producto = Producto.objects.get(id_producto=producto_data)
                pedido.productos.add(producto)
                precio_total += producto.precio
            except Producto.DoesNotExist:
                return JsonResponse({'error': f'Producto with id {producto_data} not found'}, status=404)
        pedido.precio_total = precio_total
    
    pedido.save()
    return JsonResponse(pedido.to_dict())


@api_view(['DELETE'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([HasJWTUser])
def pedido_delete(request, id_pedido):
    try:
        pedido = Pedido.objects.get(id_pedido=id_pedido)
        user = User.objects.get(username=request.user)
        if not check_admin_role(user) or user.id_user != pedido.usuario.id_user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
    except Pedido.DoesNotExist:
        return JsonResponse({'error': 'Pedido not found'}, status=404)
    
    pedido.delete()
    return JsonResponse({'message': 'Pedido deleted successfully'})