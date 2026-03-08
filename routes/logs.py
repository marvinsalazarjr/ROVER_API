# routes/logs.py
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import permiso_requerido, rol_requerido
from models.log import Log

logs_bp = Blueprint('logs', __name__)

# ── VER LOGS DE ACCIONES ──────────────────────────────────
# Solo quien tenga permiso 'ver_logs' puede acceder
@logs_bp.route('/', methods=['GET'])
@permiso_requerido('ver_logs')
def listar_logs(usuario_actual):
    filtros = {
        'accion'      : request.args.get('accion', ''),
        'usuario'     : request.args.get('usuario', ''),
        'fecha_desde' : request.args.get('fecha_desde', ''),
        'fecha_hasta' : request.args.get('fecha_hasta', ''),
    }
    logs = Log.listar(filtros)
    return jsonify({'ok': True, 'logs': logs})

# ── VER SESIONES ──────────────────────────────────────────
# Solo administrador puede ver sesiones
@logs_bp.route('/sesiones', methods=['GET'])
@rol_requerido('administrador')
def listar_sesiones(usuario_actual):
    sesiones = Log.listar_sesiones()
    return jsonify({'ok': True, 'sesiones': sesiones})

# ── ESTADÍSTICAS ──────────────────────────────────────────
@logs_bp.route('/estadisticas', methods=['GET'])
@rol_requerido('administrador')
def estadisticas(usuario_actual):
    from models.usuario import get_db
    db  = get_db()
    cur = db.cursor()
    try:
        # Total usuarios
        cur.execute("SELECT COUNT(*) as total FROM conductores WHERE activo=1")
        total_usuarios = cur.fetchone()['total']

        # Total logs
        cur.execute("SELECT COUNT(*) as total FROM logs")
        total_logs = cur.fetchone()['total']

        # Sesiones activas
        cur.execute("SELECT COUNT(*) as total FROM sesiones WHERE activa=1")
        sesiones_activas = cur.fetchone()['total']

        # Acciones más frecuentes
        cur.execute("""
            SELECT accion, COUNT(*) as total
            FROM logs
            GROUP BY accion
            ORDER BY total DESC
        """)
        acciones = cur.fetchall()

        # Últimos 5 logs
        cur.execute("""
            SELECT * FROM logs
            ORDER BY fecha DESC
            LIMIT 5
        """)
        ultimos_logs = cur.fetchall()

        return jsonify({
            'ok': True,
            'estadisticas': {
                'total_usuarios'  : total_usuarios,
                'total_logs'      : total_logs,
                'sesiones_activas': sesiones_activas,
                'acciones'        : acciones,
                'ultimos_logs'    : ultimos_logs
            }
        })
    finally:
        cur.close()
        db.close()