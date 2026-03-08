# config.py
import os
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv()

class Config:
    # ── BASE DE DATOS ──────────────────────────
    DB_HOST     = os.getenv('DB_HOST', 'localhost')
    DB_NAME     = os.getenv('DB_NAME', 'compiladores')
    DB_USER     = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_PORT     = 3306

    # ── JWT ────────────────────────────────────
    SECRET_KEY           = os.getenv('SECRET_KEY', 'rover_umg_2026')
    JWT_EXPIRATION_HOURS = 24

    # ── EMAIL ──────────────────────────────────
    MAIL_SERVER         = 'smtp.gmail.com'
    MAIL_PORT           = 587
    MAIL_USE_TLS        = True
    MAIL_USERNAME       = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD       = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME', '')

    # ── URL BASE ───────────────────────────────
    BASE_URL = 'http://localhost:5000'