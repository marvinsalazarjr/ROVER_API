# utils/carnet.py
import os
import qrcode
from reportlab.lib.pagesizes import A6, landscape
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw
from config import Config
import io

def hacer_foto_circular(ruta_imagen, tamaño=80):
    """Convierte una imagen a círculo"""
    try:
        img = Image.open(ruta_imagen).convert("RGBA")
        img = img.resize((tamaño, tamaño), Image.LANCZOS)

        mascara = Image.new('L', (tamaño, tamaño), 0)
        draw = ImageDraw.Draw(mascara)
        draw.ellipse((0, 0, tamaño, tamaño), fill=255)

        resultado = Image.new('RGBA', (tamaño, tamaño), (0, 0, 0, 0))
        resultado.paste(img, mask=mascara)

        buffer = io.BytesIO()
        resultado.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer
    except:
        return None

def generar_qr(datos):
    """Genera QR con datos del conductor"""
    qr = qrcode.QRCode(version=1, box_size=3, border=2)
    qr.add_data(datos)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="#00d4ff", back_color="white")
    buffer = io.BytesIO()
    img_qr.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

def generar_carnet(conductor_id, nickname, correo, rol, avatar=None):
    """
    Genera el carnet PDF del conductor
    Retorna la ruta del archivo generado
    """
    # Ruta donde se guarda el carnet
    carpeta = os.path.join('static', 'uploads', 'carnets')
    os.makedirs(carpeta, exist_ok=True)
    ruta_pdf = os.path.join(carpeta, f'carnet_{conductor_id}.pdf')

    # Tamaño carnet (85.6mm x 54mm — tamaño tarjeta de crédito) horizontal
    ancho  = 85.6 * mm
    alto   = 54.0 * mm

    c = canvas.Canvas(ruta_pdf, pagesize=(ancho, alto))

    # ── FONDO ──────────────────────────────────────────────
    # Fondo oscuro
    c.setFillColor(colors.HexColor('#0d0d1a'))
    c.rect(0, 0, ancho, alto, fill=1, stroke=0)

    # Franja superior degradada simulada
    c.setFillColor(colors.HexColor('#00d4ff'))
    c.rect(0, alto - 12*mm, ancho, 12*mm, fill=1, stroke=0)

    # Franja inferior
    c.setFillColor(colors.HexColor('#7b2ff7'))
    c.rect(0, 0, ancho, 6*mm, fill=1, stroke=0)

    # ── LOGO Y TÍTULO ──────────────────────────────────────
    c.setFillColor(colors.HexColor('#0d0d1a'))
    c.setFont('Helvetica-Bold', 9)
    c.drawString(3*mm, alto - 9*mm, 'UMG Basic Rover 2.0')

    c.setFont('Helvetica', 6)
    c.drawString(3*mm, alto - 13*mm, 'Credencial de Acceso')

    # ── FOTO DEL CONDUCTOR ────────────────────────────────
    foto_x = 3*mm
    foto_y = alto - 38*mm
    foto_size = 22*mm

    if avatar and os.path.exists(avatar):
        foto_circular = hacer_foto_circular(avatar, tamaño=200)
        if foto_circular:
            img_reader = ImageReader(foto_circular)
            c.drawImage(img_reader, foto_x, foto_y,
                       width=foto_size, height=foto_size, mask='auto')
    else:
        # Avatar por defecto si no hay foto
        c.setFillColor(colors.HexColor('#1a1a2e'))
        c.circle(foto_x + foto_size/2, foto_y + foto_size/2,
                foto_size/2, fill=1, stroke=0)
        c.setFillColor(colors.HexColor('#00d4ff'))
        c.setFont('Helvetica-Bold', 16)
        c.drawCentredString(foto_x + foto_size/2,
                           foto_y + foto_size/2 - 5,
                           nickname[0].upper())

    # ── DATOS DEL CONDUCTOR ───────────────────────────────
    datos_x = 28*mm

    c.setFillColor(colors.HexColor('#00d4ff'))
    c.setFont('Helvetica-Bold', 8)
    c.drawString(datos_x, alto - 18*mm, nickname.upper())

    c.setFillColor(colors.HexColor('#e0e0e0'))
    c.setFont('Helvetica', 6)
    c.drawString(datos_x, alto - 22*mm, correo)

    # Rol con badge
    colores_rol = {
        'administrador': '#ff4757',
        'editor':        '#ffa502',
        'visualizador':  '#00d4ff'
    }
    color_rol = colores_rol.get(rol, '#888888')
    c.setFillColor(colors.HexColor(color_rol))
    c.roundRect(datos_x, alto - 28*mm, 20*mm, 4*mm, 1*mm, fill=1, stroke=0)
    c.setFillColor(colors.black)
    c.setFont('Helvetica-Bold', 5)
    c.drawCentredString(datos_x + 10*mm, alto - 26*mm, rol.upper())

    # ID del conductor
    c.setFillColor(colors.HexColor('#888888'))
    c.setFont('Helvetica', 5)
    c.drawString(datos_x, alto - 32*mm, f'ID: {conductor_id:04d}')

    # ── ESPACIO DE FIRMA ──────────────────────────────────
    firma_y = 9*mm
    c.setFillColor(colors.HexColor('#1a1a2e'))
    c.roundRect(datos_x, firma_y, 35*mm, 10*mm, 1*mm, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor('#333366'))
    c.setLineWidth(0.3)
    c.roundRect(datos_x, firma_y, 35*mm, 10*mm, 1*mm, fill=0, stroke=1)
    c.setFillColor(colors.HexColor('#555555'))
    c.setFont('Helvetica', 4)
    c.drawCentredString(datos_x + 17.5*mm, firma_y + 1*mm, 'Firma Digital')

    # ── QR CODE ───────────────────────────────────────────
    qr_datos = f"UMG-ROVER|ID:{conductor_id}|{nickname}|{rol}"
    qr_buffer = generar_qr(qr_datos)
    qr_reader = ImageReader(qr_buffer)
    c.drawImage(qr_reader, ancho - 18*mm, 7*mm,
               width=15*mm, height=15*mm)

    # ── LÍNEA DECORATIVA ──────────────────────────────────
    c.setStrokeColor(colors.HexColor('#00d4ff'))
    c.setLineWidth(0.5)
    c.line(3*mm, alto - 14*mm, ancho - 3*mm, alto - 14*mm)

    c.save()
    return ruta_pdf