import qrcode
from pathlib import Path


def generate_and_save(url: str, full_save_path: Path):
    """
    Genera un QR desde una URL y lo guarda en la ruta completa especificada.
    Si la ruta no existe o algo falla, levantará (raise) una excepción que la aplicación principal (la GUI) deberá capturar.
    """
    try:
        img = qrcode.make(url)   # Generar la imagen del QR en memoria
        img.save(full_save_path) # Guardar la imagen en el disco

    except Exception as e:
        print(f"Error en qr_logic: {e}")
        raise e