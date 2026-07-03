import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import html as htmlutils
import traceback
import pprint

class ParserInterfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("ParsingCoders")
        self.root.geometry("1100x700")

        # Colores
        self.colores = {
            "bg_dark": "#1e293b",
            "primary": "#3b82f6",
            "danger": "#ef4444",
            "bg_light": "#ffffff",
            "border": "#e2e8f0",
            "invert":"#203243"
        }

        self.configurar_estilos()
        self.configurar_interfaz()
    
    def configurar_estilos(self):
        self.estilos = ttk.Style()
        self.estilos.theme_use('clam')

        #Estilos del Header
        self.estilos.configure("Header.TFrame", background=self.colores["bg_dark"])
        self.estilos.configure("Header.TLabel", background=self.colores["bg_dark"], foreground="white", font=("Segoe UI", 22, "bold"))

        # Estilos de botones
        self.estilos.configure("Primary.TButton", background=self.colores["primary"],foreground="white", font=("Segoe UI", 10))
        self.estilos.configure("Danger.TButton", background=self.colores["danger"], foreground="white", font=("Segoe UI", 10))
        self.estilos.configure("Invert.TButton", background=self.colores["invert"], foreground="white", font=("Segoe UI", 10))



    def configurar_interfaz(self):
        # 1. HEADER
        self.header = ttk.Frame(self.root, style="Header.TFrame", padding=15)
        self.header.pack(fill=tk.X)

        self.btn_cargar_archivo = ttk.Button(self.header, text="📂Cargar archivo", style="Invert.TButton", command=self.seleccionar_archivo)
        self.btn_cargar_archivo.pack(side=tk.RIGHT, padx=5)

        self.btn_parse = ttk.Button(self.header, text="🌐Parsear a HTML ", style="Primary.TButton")
        self.btn_parse.pack(side=tk.RIGHT, padx=5)

        self.btn_limpiar = ttk.Button(self.header, text="🗑️Limpiar ", style="Danger.TButton", command=self.limpiar_editor)
        self.btn_limpiar.pack(side=tk.RIGHT, padx=5)

        self.nombre = ttk.Label(self.header, text="SmartHome", style="Header.TLabel")
        self.nombre.pack(side=tk.LEFT, padx=5)


        # 2. CONTENEDOR EDITOR Y PREVIEW
        self.main_container = tk.Frame(self.root, bg=self.colores["border"])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        # Usamos frames separados para el layout de dos columnas
        self.editor = ScrolledText(self.main_container, font=("Segoe UI", 12), borderwidth=0)
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.editor.insert(tk.END,"Ingrese las instrucciones")

        self.preview = ScrolledText(self.main_container, font=("Segoe UI", 12), borderwidth=0, state='disabled')
        self.preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def seleccionar_archivo(self):
        ruta_archivo = filedialog.askopenfilename(
            parent=self.root,
            title="Elija un archivo",
            filetypes=[("SmartHome", "*.smart")]
        )
        if ruta_archivo:
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as file:
                    instrucciones = file.read()
                self.editor.delete("1.0", tk.END)
                self.editor.insert(tk.END, instrucciones)
            except FileNotFoundError:
                messagebox.showerror("Error", "No se encontró el archivo seleccionado.")
            except PermissionError:
                messagebox.showerror("Error", "No tenés permiso para abrir ese archivo.")
            except OSError as error:
                messagebox.showerror("Error", f"No se pudo abrir el archivo: {error}")
    
    def limpiar_editor(self):
        self.editor.delete("1.0", tk.END)
        


if __name__ == "__main__":
    root = tk.Tk()
    app = ParserInterfaz(root)
    root.mainloop()