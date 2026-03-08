import jwt
import datetime
import secrets
from flask import Blueprint, request, jsonify, current_app
from flask_mail import Message
from config import Config
from models.usuario import Usuario
from models.log import Log

auth_bp = Blueprint('auth', __name__)

def enviar_correo_verificacion(mail, correo, nickname, token):
    url = f"{Config.BASE_URL}/api/auth/verificar/{token}"
    msg = Message(
        subject = '✅ Verifica tu cuenta — UMG Basic Rover 2.0',
        recipients = [correo]
    )
    msg.html = f"""
    <div style="font-family:Arial;max-width:600px;margin:auto;padding:20px;background:#0d0d1a;color:#fff;border-radius:10px">
        <h1 style="color:#00d4ff;text-align:center">🚀 UMG Basic Rover 2.0</h1>
        <h2 style="text-align:center">¡Bienvenido, {nickname}!</h2>
        <p style="text-align:center">Haz clic en el botón para verificar tu cuenta:</p>
        <div style="text-align:center;margin:30px 0">
            <a href="{url}" 
               style="background:#00d4ff;color:#000;padding:14px 32px;border-radius:8px;
                      text-decoration:none;font-weight:bold;font-size:16px">
                ✅ Verificar mi cuenta
            </a>
        </div>
        <p style="color:#888;text-align:center;font-size:12px">
            Si no creaste esta cuenta, ignora este correo.
        </p>
    </div>
    """
    mail.send(msg)

# ── REGISTRO ──────────────────────────────────────────────
@auth_bp.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()

    campos = ['correo', 'correo_confirm', 'telefono', 'telefono_confirm',
              'password', 'password_confirm', 'nickname']
    for campo in campos:
        if not datos.get(campo):
            return jsonify({'ok': False, 'error': f'El campo {campo} es requerido'}), 400

    if datos['correo'] != datos['correo_confirm']:
        return jsonify({'ok': False, 'error': 'Los correos no coinciden'}), 400

    if datos['telefono'] != datos['telefono_confirm']:
        return jsonify({'ok': False, 'error': 'Los teléfonos no coinciden'}), 400

    if datos['password'] != datos['password_confirm']:
        return jsonify({'ok': False, 'error': 'Las contraseñas no coinciden'}), 400

    if len(datos['password']) < 8:
        return jsonify({'ok': False, 'error': 'La contraseña debe tener mínimo 8 caracteres'}), 400

    resultado = Usuario.crear(
        correo   = datos['correo'],
        telefono = datos['telefono'],
        password = datos['password'],
        nickname = datos['nickname'],
        avatar   = datos.get('avatar')
    )

    if not resultado['ok']:
        return jsonify(resultado), 400

    try:
        mail = current_app.extensions['mail']
        enviar_correo_verificacion(
            mail,
            datos['correo'],
            datos['nickname'],
            resultado['token']
        )
    except Exception as e:
        print(f"Error enviando correo: {e}")

    return jsonify({
        'ok': True,
        'mensaje': f"✅ Registro exitoso. Revisa tu correo {datos['correo']} para verificar tu cuenta."
    }), 201

# ── VERIFICAR CUENTA ──────────────────────────────────────
@auth_bp.route('/verificar/<token>', methods=['GET'])
def verificar(token):
    resultado = Usuario.verificar_cuenta(token)
    if resultado['ok']:
        return jsonify({
            'ok': True,
            'mensaje': '✅ Cuenta verificada correctamente. Ya puedes iniciar sesión.'
        })
    return jsonify({
        'ok': False,
        'error': 'Token inválido o cuenta ya verificada.'
    }), 400

# ── LOGIN ─────────────────────────────────────────────────
@auth_bp.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    ip    = request.remote_addr

    if not datos.get('correo') or not datos.get('password'):
        return jsonify({'ok': False, 'error': 'Correo y password son requeridos'}), 400

    usuario = Usuario.buscar_por_correo(datos['correo'])

    if not usuario:
        return jsonify({'ok': False, 'error': 'Credenciales incorrectas'}), 401

    if not usuario['verificado']:
        return jsonify({'ok': False, 'error': 'Debes verificar tu correo antes de iniciar sesión'}), 401

    if not Usuario.verificar_password(datos['password'], usuario['password']):
        return jsonify({'ok': False, 'error': 'Credenciales incorrectas'}), 401

    token = jwt.encode({
        'id'      : usuario['id'],
        'nickname': usuario['nickname'],
        'rol'     : usuario['rol'],
        'exp'     : datetime.datetime.utcnow() + datetime.timedelta(hours=Config.JWT_EXPIRATION_HOURS)
    }, Config.SECRET_KEY, algorithm='HS256')

    Log.registrar_sesion(usuario['id'], token, ip)
    Log.registrar(usuario['id'], usuario['nickname'], 'LOGIN',
                  f"Inicio de sesión desde {ip}", ip)

    permisos = Usuario.obtener_permisos(usuario['rol'])

    return jsonify({
        'ok'    : True,
        'token' : token,
        'usuario': {
            'id'      : usuario['id'],
            'nickname': usuario['nickname'],
            'correo'  : usuario['correo'],
            'rol'     : usuario['rol'],
            'avatar'  : usuario['avatar'],
            'permisos': permisos
        }
    })

# ── LOGOUT ────────────────────────────────────────────────
@auth_bp.route('/logout', methods=['POST'])
def logout():
    auth  = request.headers.get('Authorization', '')
    token = auth.split(' ')[1] if auth.startswith('Bearer ') else None
    if token:
        Log.cerrar_sesion(token)
    return jsonify({'ok': True, 'mensaje': 'Sesión cerrada correctamente'})

# ── PERFIL PROPIO ─────────────────────────────────────────
@auth_bp.route('/perfil', methods=['GET'])
def perfil():
    auth  = request.headers.get('Authorization', '')
    token = auth.split(' ')[1] if auth.startswith('Bearer ') else None

    if not token:
        return jsonify({'ok': False, 'error': 'Token requerido'}), 401

    try:
        datos    = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        usuario  = Usuario.buscar_por_id(datos['id'])
        permisos = Usuario.obtener_permisos(usuario['rol'])
        return jsonify({'ok': True, 'usuario': usuario, 'permisos': permisos})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 401

# ── OLVIDÉ MI CONTRASEÑA ──────────────────────────────────
@auth_bp.route('/recuperar', methods=['POST'])
def recuperar():
    datos  = request.get_json()
    correo = datos.get('correo')

    if not correo:
        return jsonify({'ok': False, 'error': 'El correo es requerido'}), 400

    usuario = Usuario.buscar_por_correo(correo)

    if usuario:
        token     = secrets.token_urlsafe(32)
        resultado = Usuario.guardar_token_recuperacion(correo, token)

        if resultado['ok']:
            try:
                url  = f"{Config.BASE_URL}/recuperar/{token}"
                mail = current_app.extensions['mail']
                msg  = Message(
                    subject    = '🔐 Recupera tu contraseña — UMG Basic Rover 2.0',
                    recipients = [correo]
                )
                msg.html = f"""
                <div style="font-family:Arial;max-width:600px;margin:auto;padding:20px;
                            background:#0d0d1a;color:#fff;border-radius:10px">
                    <h1 style="color:#00d4ff;text-align:center">🚀 UMG Basic Rover 2.0</h1>
                    <h2 style="text-align:center">Recuperación de contraseña</h2>
                    <p style="text-align:center">
                        Haz clic en el botón para crear una nueva contraseña.<br>
                        <small style="color:#888">Este link expira en 1 hora.</small>
                    </p>
                    <div style="text-align:center;margin:30px 0">
                        <a href="{url}"
                           style="background:#00d4ff;color:#000;padding:14px 32px;
                                  border-radius:8px;text-decoration:none;
                                  font-weight:bold;font-size:16px">
                            🔐 Cambiar contraseña
                        </a>
                    </div>
                    <p style="color:#888;text-align:center;font-size:12px">
                        Si no solicitaste esto, ignora este correo.
                    </p>
                </div>
                """
                mail.send(msg)
            except Exception as e:
                print(f"ERROR COMPLETO: {e}")
                import traceback
                traceback.print_exc()

    return jsonify({
        'ok'    : True,
        'mensaje': 'Si el correo existe, recibirás las instrucciones en breve.'
    })

# ── CAMBIAR CONTRASEÑA CON TOKEN ──────────────────────────
@auth_bp.route('/recuperar/<token>', methods=['POST'])
def cambiar_password(token):
    datos     = request.get_json()
    nueva     = datos.get('password')
    confirmar = datos.get('password_confirm')

    if not nueva or not confirmar:
        return jsonify({'ok': False, 'error': 'Todos los campos son requeridos'}), 400

    if nueva != confirmar:
        return jsonify({'ok': False, 'error': 'Las contraseñas no coinciden'}), 400

    if len(nueva) < 8:
        return jsonify({'ok': False, 'error': 'Mínimo 8 caracteres'}), 400

    usuario = Usuario.buscar_por_token_recuperacion(token)
    if not usuario:
        return jsonify({'ok': False, 'error': 'Token inválido o expirado'}), 400

    resultado = Usuario.actualizar_password(usuario['id'], nueva)
    if resultado['ok']:
        Log.registrar(
            usuario['id'],
            usuario['nickname'],
            'EDITAR',
            'Contraseña actualizada por recuperación',
            request.remote_addr
        )
        return jsonify({'ok': True, 'mensaje': '✅ Contraseña actualizada correctamente'})

    return jsonify({'ok': False, 'error': 'Error al actualizar contraseña'}), 500

# ── VERIFICAR TOKEN DE RECUPERACIÓN ──────────────────────
@auth_bp.route('/recuperar/<token>', methods=['GET'])
def verificar_token_recuperacion(token):
    usuario = Usuario.buscar_por_token_recuperacion(token)
    if not usuario:
        return jsonify({'ok': False, 'error': 'Token inválido o expirado'}), 400
    return jsonify({'ok': True, 'mensaje': 'Token válido'})