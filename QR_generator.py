import qrcode
from pathlib import Path
import sys

url = input("Introduce la url para la qr: ").strip()
filename = input("Nombre del archivo con la extension deseada (ej: 'miQR.png'): ").strip()

# Menú opciones
print("\n--- Dónde guardar ---")
print("1. Guardar en Escritorio")
print("2. Guardar en ruta específica")
opcion = input("\nSelecciona una opción (1 o 2): ").strip()

try:
    if opcion == "1":
        save_path = Path.home() / "Desktop" / filename
        print("\nGuardando en el Escritorio...")

    elif opcion == "2":
        specific_folder = input("Introduce la ruta de la carpeta: ").strip()
        save_path = Path(specific_folder) / filename
        print(f"\nGuardando en {specific_folder}...")

    else:
        print("Opción no válida.")
        sys.exit()

    # Generar y guardar imagen
    img = qrcode.make(url)
    img.save(save_path)
    print(f"\n✅ QR guardado exitosamente en: {save_path}")

except FileNotFoundError:
    print(f"\n❌ Error: La ruta o carpeta '{save_path.parent}' no existe.")
except Exception as e:
    print(f"\n❌ Error desconocido al guardar: {e}")