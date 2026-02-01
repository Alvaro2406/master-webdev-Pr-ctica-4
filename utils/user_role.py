from api_view_roles.models import Role
from viewset_usuarios.models import User

def get_user_role(username):
    try:
        user = User.objects.get(username=username)
        role = Role.objects.get(id_role=user.role.id_role)
        return role
    except (User.DoesNotExist, Role.DoesNotExist):
        return None
    

def check_admin_role(username):
    role = get_user_role(username)
    if role and role.name == 'Administrador':
        return True
    return False

def check_propietario_role(username):
    role = get_user_role(username)
    if role and role.name == 'Propietario':
        return True
    return False

def check_cliente_role(username):
    role = get_user_role(username)
    if role and role.name == 'Cliente':
        return True
    return False