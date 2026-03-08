# app.py
from flask import Flask, render_template
from flask_cors import CORS
from flask_mail import Mail
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.config['MAIL_SERVER']         = Config.MAIL_SERVER
app.config['MAIL_PORT']           = Config.MAIL_PORT
app.config['MAIL_USE_TLS']        = Config.MAIL_USE_TLS
app.config['MAIL_USERNAME']       = Config.MAIL_USERNAME
app.config['MAIL_PASSWORD']       = Config.MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = Config.MAIL_DEFAULT_SENDER

CORS(app)
mail = Mail(app)

# ── RUTAS API ─────────────────────────────────────────────
from routes.auth     import auth_bp
from routes.usuarios import usuarios_bp
from routes.logs     import logs_bp
from routes.comandos import comandos_bp        # ← NUEVO

app.register_blueprint(auth_bp,      url_prefix='/api/auth')
app.register_blueprint(usuarios_bp,  url_prefix='/api/usuarios')
app.register_blueprint(logs_bp,      url_prefix='/api/logs')
app.register_blueprint(comandos_bp,  url_prefix='/api/comandos')  # ← NUEVO

# ── RUTAS HTML ────────────────────────────────────────────
@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/editor')
def editor():
    return render_template('editor.html')

@app.route('/recuperar')
def recuperar_password():
    return render_template('recuperar.html')

@app.route('/recuperar/<token>')
def nueva_password(token):
    return render_template('nueva_password.html')

@app.route('/api')
def api_info():
    return {
        'ok'      : True,
        'mensaje' : '🚀 UMG Basic Rover 2.0 API funcionando',
        'version' : '1.0',
        'endpoints': {
            'auth'    : '/api/auth',
            'usuarios': '/api/usuarios',
            'logs'    : '/api/logs',
            'comandos': '/api/comandos'
        }
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)