from rest_framework.decorators import api_view, authentication_classes, permission_classes
from api_view_login.authentication import CookieJWTAuthentication
from django.http import JsonResponse
import json
from .models import Establecimiento
from viewset_usuarios.models import User
from utils.user_validation import HasJWTUser
from utils.user_role import check_admin_role, check_propietario_role


# Create your views here.

@api_view(['POST'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([HasJWTUser])
def establecimiento_create(request):
    
    if not check_admin_role(request.user) and not check_propietario_role(request.user):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    try: 
        json_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid Body'}, status=400)
    if 'nombre' not in json_data or 'direccion' not in json_data or 'telefono' not in json_data or 'email' not in json_data or 'id_propietario' not in json_data:
        return JsonResponse({'error': 'Missing fields'}, status=400)
    propietario_id = json_data['id_propietario']
    try:
        propietario = User.objects.get(id_user=propietario_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Propietario not found'}, status=404)
    establecimiento = Establecimiento(
        nombre=json_data['nombre'],
        direccion=json_data['direccion'],
        telefono=json_data['telefono'],
        email=json_data['email'],
        id_propietario=propietario
    )
    establecimiento.save()
    return JsonResponse(establecimiento.to_dict(), status=201)

@api_view(['GET'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([HasJWTUser])
def establecimiento_list(request):
    if not check_admin_role(request.user):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    establecimientos = Establecimiento.objects.all()
    establecimientos_list = [e.to_dict() for e in establecimientos]
    return JsonResponse(establecimientos_list, safe=False, status=200)

@api_view(['GET'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([HasJWTUser])
def establecimiento_detail(request, id_establecimiento):
    try:
        user = User.objects.get(username=request.user)
        if check_admin_role(user):
            establecimiento = Establecimiento.objects.get(id_establecimiento=id_establecimiento)
        elif check_propietario_role(user):
            establecimiento = Establecimiento.objects.get(id_establecimiento=id_establecimiento)
            if establecimiento.id_propietario != user.id_user:
                return JsonResponse({'error': 'Permission denied'}, status=403)
        
    except Establecimiento.DoesNotExist:
        return JsonResponse({'error': 'Establecimiento not found'}, status=404)
    return JsonResponse(establecimiento.to_dict(), status=200)
@api_view(['PUT'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([HasJWTUser])
def establecimiento_update(request, id_establecimiento):
    try:
        user = User.objects.get(username=request.user)
        
        if check_admin_role(user):
            
            establecimiento = Establecimiento.objects.get(id_establecimiento=id_establecimiento)
        elif check_propietario_role(user):
            print("ENTRA EN PROPIETARIO")
            establecimiento = Establecimiento.objects.get(id_establecimiento=id_establecimiento)
            if establecimiento.id_propietario != user.id_user:
                return JsonResponse({'error': 'Permission denied'}, status=403)
    except Establecimiento.DoesNotExist:
        return JsonResponse({'error': 'Establecimiento not found'}, status=404)
    
    if not check_admin_role(request.user) and not check_propietario_role(request.user):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    try: 
        json_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid Body'}, status=400)
    for field in ['nombre', 'direccion', 'telefono', 'email', 'id_propietario']:
        if field in json_data:
            if field == 'id_propietario':
                try:
                    propietario = User.objects.get(id_user=json_data[field])
                    establecimiento.id_propietario = propietario
                except User.DoesNotExist:
                    return JsonResponse({'error': 'Propietario not found'}, status=404)
            else:
                setattr(establecimiento, field, json_data[field])
    establecimiento.save()
    return JsonResponse(establecimiento.to_dict(), status=200)

@api_view(['DELETE'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([HasJWTUser])
def establecimiento_delete(request, id_establecimiento):
    if not check_admin_role(request.user):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    try:
        establecimiento = Establecimiento.objects.get(id_establecimiento=id_establecimiento)
    except Establecimiento.DoesNotExist:
        return JsonResponse({'error': 'Establecimiento not found'}, status=404)
    establecimiento.delete()
    return JsonResponse({'message': 'Establecimiento deleted successfully'}, status=200)
