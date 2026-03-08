// static/js/api.js
const API_URL = window.location.origin;

// ── UTILIDADES ────────────────────────────────────────────

// Guardar token en localStorage
function guardarSesion(token, usuario) {
    localStorage.setItem('token', token);
    localStorage.setItem('usuario', JSON.stringify(usuario));
}

// Obtener token
function getToken() {
    return localStorage.getItem('token');
}

// Obtener usuario actual
function getUsuario() {
    const u = localStorage.getItem('usuario');
    return u ? JSON.parse(u) : null;
}

// Cerrar sesión local
function limpiarSesion() {
    localStorage.removeItem('token');
    localStorage.removeItem('usuario');
}

// Verificar si está logueado
function estaLogueado() {
    return !!getToken();
}

// Redirigir si no está logueado
function requiereAuth() {
    if (!estaLogueado()) {
        window.location.href = '/login';
    }
}

// Redirigir si ya está logueado
function redirigirSiLogueado() {
    if (estaLogueado()) {
        window.location.href = '/dashboard';
    }
}

// Mostrar alerta
function mostrarAlerta(id, mensaje, tipo) {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = mensaje;
    el.className   = `alerta ${tipo} show`;
    setTimeout(() => el.classList.remove('show'), 5000);
}

// Headers con token
function headersAuth() {
    return {
        'Content-Type' : 'application/json',
        'Authorization': `Bearer ${getToken()}`
    };
}

// ── LLAMADAS A LA API ─────────────────────────────────────

// Registro
async function registrar(datos) {
    const res = await fetch(`${API_URL}/api/auth/registro`, {
        method  : 'POST',
        headers : { 'Content-Type': 'application/json' },
        body    : JSON.stringify(datos)
    });
    return res.json();
}

// Login
async function login(correo, password) {
    const res = await fetch(`${API_URL}/api/auth/login`, {
        method  : 'POST',
        headers : { 'Content-Type': 'application/json' },
        body    : JSON.stringify({ correo, password })
    });
    return res.json();
}

// Logout
async function logout() {
    await fetch(`${API_URL}/api/auth/logout`, {
        method  : 'POST',
        headers : headersAuth()
    });
    limpiarSesion();
    window.location.href = '/login';
}

// Obtener logs
async function getLogs(filtros = {}) {
    const params = new URLSearchParams(filtros).toString();
    const res = await fetch(`${API_URL}/api/logs/?${params}`, {
        headers: headersAuth()
    });
    return res.json();
}

// Obtener estadísticas
async function getEstadisticas() {
    const res = await fetch(`${API_URL}/api/logs/estadisticas`, {
        headers: headersAuth()
    });
    return res.json();
}

// Obtener usuarios
async function getUsuarios() {
    const res = await fetch(`${API_URL}/api/usuarios/`, {
        headers: headersAuth()
    });
    return res.json();
}

// Cambiar rol
async function cambiarRol(id, rol) {
    const res = await fetch(`${API_URL}/api/usuarios/${id}/rol`, {
        method  : 'PUT',
        headers : headersAuth(),
        body    : JSON.stringify({ rol })
    });
    return res.json();
}

// Obtener sesiones
async function getSesiones() {
    const res = await fetch(`${API_URL}/api/logs/sesiones`, {
        headers: headersAuth()
    });
    return res.json();
}