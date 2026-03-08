# routes/comandos.py
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_requerido, permiso_requerido
from models.comando import Comando
from models.log import Log

comandos_bp = Blueprint('comandos', __name__)

# ── VER COMANDOS ──────────────────────────────────────────
# Todos los roles pueden ver comandos
@comandos_bp.route('/', methods=['GET'])
@permiso_requerido('ver_comandos')
def listar(usuario_actual):
    comandos = Comando.listar(
        conductor_id = usuario_actual['id'],
        rol          = usuario_actual['rol']
    )
    return jsonify({'ok': True, 'comandos': comandos})

# ── CREAR COMANDO ─────────────────────────────────────────
# Solo administrador y editor pueden escribir comandos
@comandos_bp.route('/', methods=['POST'])
@permiso_requerido('escribir_comandos')
def crear(usuario_actual):
    datos  = request.get_json()
    nombre = datos.get('nombre', '').strip()
    codigo = datos.get('codigo', '').strip()

    if not nombre or not codigo:
        return jsonify({'ok': False, 'error': 'Nombre y código son requeridos'}), 400

    # Validar estructura básica UMG++
    if 'PROGRAM' not in codigo or 'BEGIN' not in codigo or 'END' not in codigo:
        return jsonify({
            'ok'   : False,
            'error': 'El código debe tener estructura UMG++: PROGRAM, BEGIN y END'
        }), 400

    resultado = Comando.crear(
        conductor_id = usuario_actual['id'],
        nickname     = usuario_actual['nickname'],
        nombre       = nombre,
        codigo       = codigo
    )

    if resultado['ok']:
        Log.registrar(
            usuario_actual['id'],
            usuario_actual['nickname'],
            'CREAR',
            f"Creó comando '{nombre}'",
            request.remote_addr
        )

    return jsonify(resultado), 201 if resultado['ok'] else 400

# ── ENVIAR COMANDO AL ROVER ───────────────────────────────
# Solo administrador y editor pueden enviar
@comandos_bp.route('/<int:id>/enviar', methods=['POST'])
@permiso_requerido('enviar_comandos')
def enviar(usuario_actual, id):
    resultado = Comando.enviar(id, usuario_actual['id'])

    if resultado['ok']:
        Log.registrar(
            usuario_actual['id'],
            usuario_actual['nickname'],
            'EDITAR',
            f"Envió comando ID {id} al Rover",
            request.remote_addr
        )
        return jsonify({
            'ok'     : True,
            'mensaje': f"✅ Comando enviado al Rover correctamente",
            'comando': resultado['comando']
        })

    return jsonify(resultado), 400

# ── VER UN COMANDO ────────────────────────────────────────
@comandos_bp.route('/<int:id>', methods=['GET'])
@permiso_requerido('ver_comandos')
def ver(usuario_actual, id):
    comando = Comando.obtener(id)
    if not comando:
        return jsonify({'ok': False, 'error': 'Comando no encontrado'}), 404

    # Visualizador solo puede ver sus propios comandos
    if usuario_actual['rol'] == 'visualizador' and comando['conductor_id'] != usuario_actual['id']:
        return jsonify({'ok': False, 'error': 'Acceso denegado'}), 403

    return jsonify({'ok': True, 'comando': comando})

# ── ELIMINAR COMANDO ──────────────────────────────────────
@comandos_bp.route('/<int:id>', methods=['DELETE'])
@permiso_requerido('escribir_comandos')
def eliminar(usuario_actual, id):
    resultado = Comando.eliminar(id, usuario_actual['id'], usuario_actual['rol'])

    if resultado['ok']:
        Log.registrar(
            usuario_actual['id'],
            usuario_actual['nickname'],
            'ELIMINAR',
            f"Eliminó comando ID {id}",
            request.remote_addr
        )
        return jsonify({'ok': True, 'mensaje': 'Comando eliminado'})

    return jsonify({'ok': False, 'error': 'Comando no encontrado o sin permiso'}), 404