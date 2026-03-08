# middleware/auth_middleware.py
import jwt
from functools import wraps
from flask import request, jsonify
from config import Config
from models.usuario import Usuario

def token_requerido(f):
    """
    Decorador que verifica que el request tenga un token JWT válido.
    Uso: @token_requerido encima de cualquier ruta protegida
    """
    @wraps(f)
    def decorador(*args, **kwargs):
        token = None

        # Buscar token en el header Authorization
        if 'Authorization' in request.headers:
            auth = request.headers['Authorization']
            if auth.startswith('Bearer '):
                token = auth.split(' ')[1]

        if not token:
            return jsonify({
                'ok': False,
                'error': 'Token requerido'
            }), 401

        try:
            # Decodificar y verificar el token
            datos = jwt.decode(
                token,
                Config.SECRET_KEY,
                algorithms=['HS256']
            )
            # Buscar el usuario en la BD
            usuario_actual = Usuario.buscar_por_id(datos['id'])
            if not usuario_actual:
                return jsonify({'ok': False, 'error': 'Usuario no encontrado'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'ok': False, 'error': 'Token expirado, inicia sesión nuevamente'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'ok': False, 'error': 'Token inválido'}), 401

        # Pasar el usuario actual a la función
        return f(usuario_actual, *args, **kwargs)

    return decorador


def rol_requerido(*roles):
    """
    Decorador que verifica que el usuario tenga el rol necesario.
    Uso: @rol_requerido('administrador') o @rol_requerido('administrador', 'editor')
    """
    def decorador(f):
        @wraps(f)
        @token_requerido
        def wrapper(usuario_actual, *args, **kwargs):
            if usuario_actual['rol'] not in roles:
                return jsonify({
                    'ok': False,
                    'error': f"Acceso denegado. Se requiere rol: {', '.join(roles)}"
                }), 403
            return f(usuario_actual, *args, **kwargs)
        return wrapper
    return decorador


def permiso_requerido(permiso):
    """
    Decorador que verifica que el usuario tenga un permiso específico.
    Uso: @permiso_requerido('ver_logs')
    """
    def decorador(f):
        @wraps(f)
        @token_requerido
        def wrapper(usuario_actual, *args, **kwargs):
            permisos = Usuario.obtener_permisos(usuario_actual['rol'])
            if permiso not in permisos:
                return jsonify({
                    'ok': False,
                    'error': f"No tienes permiso para: {permiso}"
                }), 403
            return f(usuario_actual, *args, **kwargs)
        return wrapper
    return decorador