# models/usuario.py
import pymysql
import bcrypt
import secrets
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

class Usuario:

    # ── CREAR USUARIO ──────────────────────────────────────
    @staticmethod
    def crear(correo, telefono, password, nickname, avatar=None):
        db  = get_db()
        cur = db.cursor()
        try:
            password_hash = bcrypt.hashpw(
                password.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

            token = secrets.token_urlsafe(32)

            cur.execute("""
                INSERT INTO conductores 
                    (correo, telefono, password, nickname, avatar, token_verificacion)
                VALUES 
                    (%s, %s, %s, %s, %s, %s)
            """, (correo, telefono, password_hash, nickname, avatar, token))

            db.commit()
            return {'ok': True, 'token': token, 'id': cur.lastrowid}

        except pymysql.IntegrityError as e:
            if 'correo' in str(e):
                return {'ok': False, 'error': 'El correo ya está registrado'}
            if 'nickname' in str(e):
                return {'ok': False, 'error': 'El nickname ya está en uso'}
            return {'ok': False, 'error': str(e)}
        finally:
            cur.close()
            db.close()

    # ── VERIFICAR CUENTA ───────────────────────────────────
    @staticmethod
    def verificar_cuenta(token):
        db  = get_db()
        cur = db.cursor()
        try:
            cur.execute("""
                UPDATE conductores 
                SET verificado = 1, token_verificacion = NULL
                WHERE token_verificacion = %s AND verificado = 0
            """, (token,))
            db.commit()
            return {'ok': cur.rowcount > 0}
        finally:
            cur.close()
            db.close()

    # ── BUSCAR POR CORREO ──────────────────────────────────
    @staticmethod
    def buscar_por_correo(correo):
        db  = get_db()
        cur = db.cursor()
        try:
            cur.execute(
                "SELECT * FROM conductores WHERE correo = %s AND activo = 1",
                (correo,)
            )
            return cur.fetchone()
        finally:
            cur.close()
            db.close()

    # ── BUSCAR POR ID ──────────────────────────────────────
    @staticmethod
    def buscar_por_id(id):
        db  = get_db()
        cur = db.cursor()
        try:
            cur.execute(
                "SELECT id, correo, telefono, nickname, avatar, rol, verificado, creado_en FROM conductores WHERE id = %s",
                (id,)
            )
            return cur.fetchone()
        finally:
            cur.close()
            db.close()

    # ── VERIFICAR PASSWORD ─────────────────────────────────
    @staticmethod
    def verificar_password(password_plano, password_hash):
        return bcrypt.checkpw(
            password_plano.encode('utf-8'),
            password_hash.encode('utf-8')
        )

    # ── LISTAR TODOS ───────────────────────────────────────
    @staticmethod
    def listar():
        db  = get_db()
        cur = db.cursor()
        try:
            cur.execute("""
                SELECT id, correo, telefono, nickname, avatar, rol, verificado, activo, creado_en 
                FROM conductores 
                ORDER BY creado_en DESC
            """)
            return cur.fetchall()
        finally:
            cur.close()
            db.close()

    # ── OBTENER PERMISOS ───────────────────────────────────
    @staticmethod
    def obtener_permisos(rol):
        db  = get_db()
        cur = db.cursor()
        try:
            cur.execute(
                "SELECT permiso FROM permisos WHERE rol = %s",
                (rol,)
            )
            return [row['permiso'] for row in cur.fetchall()]
        finally:
            cur.close()
            db.close()

    # ── GUARDAR TOKEN DE RECUPERACIÓN ─────────────────────
    @staticmethod
    def guardar_token_recuperacion(correo, token):
        db  = get_db()
        cur = db.cursor()
        try:
            cur.execute("""
                UPDATE conductores
                SET token_recuperacion = %s,
                    token_recuperacion_exp = DATE_ADD(NOW(), INTERVAL 1 HOUR)
                WHERE correo = %s AND activo = 1
            """, (token, correo))
            db.commit()
            return {'ok': cur.rowcount > 0}
        finally:
            cur.close()
            db.close()

    # ── BUSCAR POR TOKEN DE RECUPERACIÓN ──────────────────
    @staticmethod
    def buscar_por_token_recuperacion(token):
        db  = get_db()
        cur = db.cursor()
        try:
            cur.execute("""
                SELECT * FROM conductores
                WHERE token_recuperacion = %s
                AND token_recuperacion_exp > NOW()
                AND activo = 1
            """, (token,))
            return cur.fetchone()
        finally:
            cur.close()
            db.close()

    # ── ACTUALIZAR CONTRASEÑA ──────────────────────────────
    @staticmethod
    def actualizar_password(id, nueva_password):
        db  = get_db()
        cur = db.cursor()
        try:
            password_hash = bcrypt.hashpw(
                nueva_password.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

            cur.execute("""
                UPDATE conductores
                SET password = %s,
                    token_recuperacion = NULL,
                    token_recuperacion_exp = NULL
                WHERE id = %s
            """, (password_hash, id))
            db.commit()
            return {'ok': cur.rowcount > 0}
        finally:
            cur.close(
                
            )
            db.close()