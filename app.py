import customtkinter as ctk
from pathlib import Path
from PIL import Image
import qr_logic


# --- Apariencia ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class QRApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # -------------  Ventana Principal -------------  #
        self.title("Generador QR")
        self.geometry("600x700")  # Ancho x Alto
        self.resizable(False, False)  # Evita que se pueda cambiar el tamaño
        self.center_window()


        # ------------- Widgets ------------- #

        ### URL ###
        # Título
        self.label_url = ctk.CTkLabel(self, text="Introduce la URL aquí", font=("Arial", 14, "bold"))
        self.label_url.pack(pady=(20, 5), padx=30, anchor="w")  # alinea a la izquierda

        # Campo de entrada
        self.entry_url = ctk.CTkEntry(self, placeholder_text="https://www.ejemplo.com", width=440)
        self.entry_url.pack(pady=0, padx=30, fill="x")

        ### RUTA ###
        self.label_path = ctk.CTkLabel(self, text="Dónde desea guardar", font=("Arial", 14, "bold"))
        self.label_path.pack(pady=(20, 5), padx=30, anchor="w")

        # Frame para alinear la entrada de ruta y el botón "..."
        self.path_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.path_frame.pack(pady=0, padx=30, fill="x")
        self.path_frame.grid_columnconfigure(0, weight=1)

        # Campo de entrada
        self.entry_path = ctk.CTkEntry(self.path_frame, placeholder_text="Selecciona carpeta...")
        self.entry_path.grid(row=0, column=0, sticky="we")

        # Botón "..." para buscar carpeta
        self.btn_browse = ctk.CTkButton(self.path_frame, text="...", width=50, command=self.browse_folder)
        self.btn_browse.grid(row=0, column=1, padx=(10, 0))

        ### NOMBRE ARCHIVO ###
        self.label_name = ctk.CTkLabel(self, text="Nombre del archivo", font=("Arial", 12, "bold"))
        self.label_name.pack(pady=(15, 5), padx=30, anchor="w")

        self.entry_name = ctk.CTkEntry(self, placeholder_text="miQR.png")
        self.entry_name.pack(pady=0, padx=30, fill="x")

        ### BOTÓN GENERAR QR ###
        self.btn_generate = ctk.CTkButton(self, text="GENERAR QR", height=30, font=("Arial", 13, "bold"), command=self.generate_qr)
        self.btn_generate.pack(pady=30, padx=30)

        ### ÁREA DE PREVISUALIZACIÓN DEL QR ###
        self.label_preview_title = ctk.CTkLabel(self, text="Código QR generado", text_color="gray")
        self.label_preview_title.pack(pady=10)

        # Label para mostrar la imagen del QR
        self.qr_preview_label = ctk.CTkLabel(self, text="", fg_color="#E0E0E0", width=250, height=250)
        self.qr_preview_label.pack(pady=10)

        # Etiqueta de estado
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=(5, 10))

        # Guardamos el color de borde por defecto para resetearlo
        self.default_border_color = self.entry_url.cget("border_color")


    # --- LÓGICA --- #

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')


    def browse_folder(self):
        folder_selected = ctk.filedialog.askdirectory()
        if folder_selected:
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, folder_selected)
            self.entry_path.configure(border_color=self.default_border_color)


    def generate_qr(self):
        # 1. Resetear estado de la UI
        self.status_label.configure(text="")
        self.entry_url.configure(border_color=self.default_border_color)
        self.entry_path.configure(border_color=self.default_border_color)

        # 2. Recoger datos de la GUI
        url = self.entry_url.get().strip()
        path_text = self.entry_path.get().strip()
        filename = self.entry_name.get().strip()

        # Funcionalidades extras y señalización e incorrecto uso
        if not filename:
            filename = "miQR.png"
        if not filename.endswith(".png"):
            filename += ".png"

        if not url:
            self.status_label.configure(text="Error: debes introducir una URL", text_color="red")
            self.entry_url.configure(border_color="red")
            return

        if not path_text:
            self.status_label.configure(text="Error: debes introducir una carpeta", text_color="red")
            self.entry_path.configure(border_color="red")
            return

        try:
            save_path = Path(path_text) / filename

            #Llamamos función generar QR
            qr_logic.generate_and_save(url, save_path)

            self.status_label.configure(text=f"Guardado en {save_path.parent.name}", text_color="green")

            with Image.open(save_path) as img:
                img.load()  # Carga la data
                imagen_qr = img.copy()  # Crea una copia en memoria

            mostrar_preview = ctk.CTkImage(light_image=imagen_qr, dark_image=imagen_qr, size=(250, 250))
            self.qr_preview_label.configure(image=mostrar_preview)

        except FileNotFoundError:
            self.status_label.configure(text="Error: La ruta de carpeta no existe", text_color="red")
            self.entry_path.configure(border_color="red")
        except Exception as e:
            self.status_label.configure(text=f"Error desconocido: {e}", text_color="red")


# --- Ejecutar la aplicación --- #
if __name__ == "__main__":
    app = QRApp()  # Crea la instancia de la aplicación
    app.mainloop()  # Mantiene la ventana abierta