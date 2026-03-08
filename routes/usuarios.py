# routes/usuarios.py
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_requerido, rol_requerido
from models.usuario import Usuario
from models.log import Log

usuarios_bp = Blueprint('usuarios', __name__)

# ── LISTAR TODOS LOS USUARIOS ─────────────────────────────
# Solo administrador puede ver todos los usuarios
@usuarios_bp.route('/', methods=['GET'])
@rol_requerido('administrador')
def listar(usuario_actual):
    usuarios = Usuario.listar()
    return jsonify({'ok': True, 'usuarios': usuarios})

# ── VER UN USUARIO ────────────────────────────────────────
@usuarios_bp.route('/<int:id>', methods=['GET'])
@token_requerido
def ver(usuario_actual, id):
    # Solo admin puede ver cualquier usuario
    # Un usuario normal solo puede verse a sí mismo
    if usuario_actual['rol'] != 'administrador' and usuario_actual['id'] != id:
        return jsonify({'ok': False, 'error': 'Acceso denegado'}), 403

    usuario = Usuario.buscar_por_id(id)
    if not usuario:
        return jsonify({'ok': False, 'error': 'Usuario no encontrado'}), 404

    return jsonify({'ok': True, 'usuario': usuario})

# ── CAMBIAR ROL ───────────────────────────────────────────
# Solo administrador puede cambiar roles
@usuarios_bp.route('/<int:id>/rol', methods=['PUT'])
@rol_requerido('administrador')
def cambiar_rol(usuario_actual, id):
    datos = request.get_json()
    nuevo_rol = datos.get('rol')

    roles_validos = ['administrador', 'editor', 'visualizador']
    if nuevo_rol not in roles_validos:
        return jsonify({
            'ok': False,
            'error': f"Rol inválido. Debe ser: {', '.join(roles_validos)}"
        }), 400

    from models.usuario import get_db
    db  = get_db()
    cur = db.cursor()
    try:
        cur.execute(
            "UPDATE conductores SET rol = %s WHERE id = %s",
            (nuevo_rol, id)
        )
        db.commit()

        if cur.rowcount == 0:
            return jsonify({'ok': False, 'error': 'Usuario no encontrado'}), 404

        # Registrar en log
        Log.registrar(
            usuario_actual['id'],
            usuario_actual['nickname'],
            'EDITAR',
            f"Cambió rol del usuario ID {id} a '{nuevo_rol}'",
            request.remote_addr
        )

        return jsonify({'ok': True, 'mensaje': f"Rol actualizado a '{nuevo_rol}'"})
    finally:
        cur.close()
        db.close()

# ── DESACTIVAR USUARIO ────────────────────────────────────
@usuarios_bp.route('/<int:id>/desactivar', methods=['PUT'])
@rol_requerido('administrador')
def desactivar(usuario_actual, id):
    if usuario_actual['id'] == id:
        return jsonify({'ok': False, 'error': 'No puedes desactivarte a ti mismo'}), 400

    from models.usuario import get_db
    db  = get_db()
    cur = db.cursor()
    try:
        cur.execute(
            "UPDATE conductores SET activo = 0 WHERE id = %s",
            (id,)
        )
        db.commit()

        if cur.rowcount == 0:
            return jsonify({'ok': False, 'error': 'Usuario no encontrado'}), 404

        Log.registrar(
            usuario_actual['id'],
            usuario_actual['nickname'],
            'ELIMINAR',
            f"Desactivó al usuario ID {id}",
            request.remote_addr
        )

        return jsonify({'ok': True, 'mensaje': 'Usuario desactivado'})
    finally:
        cur.close()
        db.close()

# ── ACTIVAR USUARIO ───────────────────────────────────────
@usuarios_bp.route('/<int:id>/activar', methods=['PUT'])
@rol_requerido('administrador')
def activar(usuario_actual, id):
    from models.usuario import get_db
    db  = get_db()
    cur = db.cursor()
    try:
        cur.execute(
            "UPDATE conductores SET activo = 1 WHERE id = %s",
            (id,)
        )
        db.commit()

        Log.registrar(
            usuario_actual['id'],
            usuario_actual['nickname'],
            'EDITAR',
            f"Activó al usuario ID {id}",
            request.remote_addr
        )

        return jsonify({'ok': True, 'mensaje': 'Usuario activado'})
    finally:
        cur.close()
        db.close()

# ── MIS PERMISOS ──────────────────────────────────────────
@usuarios_bp.route('/mis-permisos', methods=['GET'])
@token_requerido
def mis_permisos(usuario_actual):
    permisos = Usuario.obtener_permisos(usuario_actual['rol'])
    return jsonify({
        'ok'      : True,
        'rol'     : usuario_actual['rol'],
        'permisos': permisos
    })