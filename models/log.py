# models/log.py
import pymysql
from config import Config

def get_db():
    return pymysql.connect(
        host        = Config.DB_HOST,
        user        = Config.DB_USER,
        password    = Config.DB_PASSWORD,
        database    = Config.DB_NAME,
        charset     = 'utf8mb4',
        cursorclass = pymysql.cursors.DictCursor
    )

class Log:

    # ── REGISTRAR ACCIÓN ───────────────────────────────────
    @staticmethod
    def registrar(conductor_id, nickname, accion, descripcion='', ip=None):
        db  = get_db()
        cur = db.cursor()
        try:
            cur.execute("""
                INSERT INTO logs
                    (usuario_id, usuario_nombre, accion, descripcion, ip_address)
                VALUES
                    (%s, %s, %s, %s, %s)
            """, (conductor_id, nickname, accion.upper(), descripcion, ip))
            db.commit()
            return {'ok': True}
        except Exception as e:
            return {'ok': False, 'error': str(e)}
        finally:
            cur.close()
            db.close()

    # ── REGISTRAR SESIÓN ───────────────────────────────────
    @staticmethod
    def registrar_sesion(conductor_id, token, ip=None):
        db  = get_db()
        cur = db.cursor()
        try:
            cur.execute("""
                INSERT INTO sesiones
                    (conductor_id, token, ip_address)
                VALUES
                    (%s, %s, %s)
            """, (conductor_id, token, ip))
            db.commit()
            return {'ok': True, 'sesion_id': cur.lastrowid}
        except Exception as e:
            return {'ok': False, 'error': str(e)}
        finally:
            cur.close()
            db.close()

    # ── CERRAR SESIÓN ──────────────────────────────────────
    @staticmethod
    def cerrar_sesion(token):
        db  = get_db()
        cur = db.cursor()
        try:
            cur.execute("""
                UPDATE sesiones
                SET activa = 0, fecha_salida = NOW()
                WHERE token = %s AND activa = 1
            """, (token,))
            db.commit()
            return {'ok': True}
        except Exception as e:
            return {'ok': False, 'error': str(e)}
        finally:
            cur.close()
            db.close()

    # ── LISTAR LOGS ────────────────────────────────────────
    @staticmethod
    def listar(filtros={}):
        db  = get_db()
        cur = db.cursor()
        try:
            sql    = "SELECT * FROM logs WHERE 1=1"
            params = []

            if filtros.get('accion'):
                sql += " AND accion = %s"
                params.append(filtros['accion'].upper())

            if filtros.get('usuario'):
                sql += " AND usuario_nombre LIKE %s"
                params.append(f"%{filtros['usuario']}%")

            if filtros.get('fecha_desde'):
                sql += " AND fecha >= %s"
                params.append(filtros['fecha_desde'] + ' 00:00:00')

            if filtros.get('fecha_hasta'):
                sql += " AND fecha <= %s"
                params.append(filtros['fecha_hasta'] + ' 23:59:59')

            sql += " ORDER BY fecha DESC LIMIT 200"
            cur.execute(sql, params)
            return cur.fetchall()
        finally:
            cur.close()
            db.close()

    # ── LISTAR SESIONES ────────────────────────────────────
    @staticmethod
    def listar_sesiones():
        db  = get_db()
        cur = db.cursor()
        try:
            cur.execute("""
                SELECT 
                    s.id,
                    c.nickname,
                    c.avatar,
                    c.correo,
                    s.ip_address,
                    s.fecha_ingreso,
                    s.fecha_salida,
                    s.activa
                FROM sesiones s
                JOIN conductores c ON c.id = s.conductor_id
                ORDER BY s.fecha_ingreso DESC
            """)
            return cur.fetchall()
        finally:
            cur.close()
            db.close()