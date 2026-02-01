from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import AuthenticationFailed
from viewset_usuarios.models import User

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("access")
        if not token:
            return None

        try:
            validated_token = self.get_validated_token(token)
        except InvalidToken as e:
            raise AuthenticationFailed("Invalid token") from e

        user_id = validated_token.get("user_id")
        user = User.objects.get(id_user=user_id)
        return (user, validated_token)