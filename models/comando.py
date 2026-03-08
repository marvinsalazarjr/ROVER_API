# models/comando.py
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

class Comando:

    # ── CREAR COMANDO ──────────────────────────────────────
    @staticmethod
    def crear(conductor_id, nickname, nombre, codigo):
        db  = get_db()
        cur = db.cursor()
        try:
            cur.execute("""
                INSERT INTO comandos
                    (conductor_id, nickname, nombre, codigo)
                VALUES
                    (%s, %s, %s, %s)
            """, (conductor_id, nickname, nombre, codigo))
            db.commit()
            return {'ok': True, 'id': cur.lastrowid}
        except Exception as e:
            return {'ok': False, 'error': str(e)}
        finally:
            cur.close()
            db.close()

    # ── ENVIAR COMANDO ─────────────────────────────────────
    @staticmethod
    def enviar(id, conductor_id):
        db  = get_db()
        cur = db.cursor()
        try:
            # Verificar que el comando pertenece al conductor
            cur.execute("""
                SELECT * FROM comandos
                WHERE id = %s AND conductor_id = %s
            """, (id, conductor_id))
            comando = cur.fetchone()

            if not comando:
                return {'ok': False, 'error': 'Comando no encontrado'}

            cur.execute("""
                UPDATE comandos
                SET estado = 'enviado', fecha_envio = NOW()
                WHERE id = %s
            """, (id,))
            db.commit()
            return {'ok': True, 'comando': comando}
        except Exception as e:
            return {'ok': False, 'error': str(e)}
        finally:
            cur.close()
            db.close()

    # ── LISTAR COMANDOS ────────────────────────────────────
    @staticmethod
    def listar(conductor_id=None, rol=None):
        db  = get_db()
        cur = db.cursor()
        try:
            # Admin ve todos, editor y visualizador solo los suyos
            if rol == 'administrador':
                cur.execute("""
                    SELECT * FROM comandos
                    ORDER BY fecha_creacion DESC
                """)
            else:
                cur.execute("""
                    SELECT * FROM comandos
                    WHERE conductor_id = %s
                    ORDER BY fecha_creacion DESC
                """, (conductor_id,))
            return cur.fetchall()
        finally:
            cur.close()
            db.close()

    # ── OBTENER UN COMANDO ─────────────────────────────────
    @staticmethod
    def obtener(id):
        db  = get_db()
        cur = db.cursor()
        try:
            cur.execute("SELECT * FROM comandos WHERE id = %s", (id,))
            return cur.fetchone()
        finally:
            cur.close()
            db.close()

    # ── ELIMINAR COMANDO ───────────────────────────────────
    @staticmethod
    def eliminar(id, conductor_id, rol):
        db  = get_db()
        cur = db.cursor()
        try:
            if rol == 'administrador':
                cur.execute("DELETE FROM comandos WHERE id = %s", (id,))
            else:
                cur.execute("""
                    DELETE FROM comandos
                    WHERE id = %s AND conductor_id = %s
                """, (id, conductor_id))
            db.commit()
            return {'ok': cur.rowcount > 0}
        except Exception as e:
            return {'ok': False, 'error': str(e)}
        finally:
            cur.close()
            db.close()