from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from viewset_usuarios.models import User
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid body"}, status=400)


    if 'username' not in data or 'password' not in data:
        return JsonResponse({"error": "Missing fields"}, status=400)

    try:
        username = data["username"]
        password = data["password"]
        user = User.objects.get(username=username)
        
    except User.DoesNotExist:
        
        return JsonResponse({"error": "Invalid username"}, status=401)

    
    if str(user.password) != str(password):
        return JsonResponse({"error": "Invalid password"}, status=401)

    refresh = RefreshToken.for_user(user)
    refresh["user_id"] = user.id_user
    refresh["username"] = user.username

    response = JsonResponse({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user_id": user.id_user,
    }, status=200)
    
    response.set_cookie(
        key="access",
        value=str(refresh.access_token),
        httponly=True,
        secure=False,
        samesite="Strict",
    )
    return response

