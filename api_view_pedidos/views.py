from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Pedido
from viewset_usuarios.models import User
from viewset_productos.models import Producto

# Create your views here.

@csrf_exempt
@require_http_methods(["POST"])
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


@require_http_methods(["GET"])
def pedido_list(request):
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

@require_http_methods(["GET"])
def pedido_detail(request, id_pedido):
    try:
        pedido = Pedido.objects.get(id_pedido=id_pedido)
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


@csrf_exempt
@require_http_methods(["PUT"])
def pedido_update(request, id_pedido):
    try: 
        json_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid Body'}, status=400)
    
    try:
        pedido = Pedido.objects.get(id_pedido=id_pedido)
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


@csrf_exempt
@require_http_methods(["DELETE"])
def pedido_delete(request, id_pedido):
    try:
        pedido = Pedido.objects.get(id_pedido=id_pedido)
    except Pedido.DoesNotExist:
        return JsonResponse({'error': 'Pedido not found'}, status=404)
    
    pedido.delete()
    return JsonResponse({'message': 'Pedido deleted successfully'})