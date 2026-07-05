import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import html as htmlutils
import os
from parser import SmartHomeParser

class ParserInterfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("TPI UTN FRRE - Smart-Home System")
        self.root.geometry("1100x700")
        self.ruta_archivo_actual = None
        self.compilador = SmartHomeParser()
        
        # Colores fusionados con los del compañero
        self.colores = {
            "bg_dark": "#1e293b",
            "btn_cargar": "#2980b9",  # Azul del compañero
            "btn_analizar": "#d35400", # Naranja del compañero
            "danger": "#ef4444",
            "border": "#e2e8f0"
        }

        self.configurar_estilos()
        self.configurar_interfaz()
    
    def configurar_estilos(self):
        self.estilos = ttk.Style()
        self.estilos.theme_use('clam')

        self.estilos.configure("Header.TFrame", background=self.colores["bg_dark"])
        self.estilos.configure("Header.TLabel", background=self.colores["bg_dark"], foreground="white", font=("Segoe UI", 22, "bold"))
        self.estilos.configure("Danger.TButton", background=self.colores["danger"], foreground="white", font=("Segoe UI", 10, "bold"))

    def configurar_interfaz(self):
        # 1. HEADER
        self.header = ttk.Frame(self.root, style="Header.TFrame", padding=15)
        self.header.pack(fill=tk.X)

        self.nombre = ttk.Label(self.header, text="SmartHome", style="Header.TLabel")
        self.nombre.pack(side=tk.LEFT, padx=5)

        # Botones con estilo del compañero usando tk.Button para aceptar bg color directo
        self.btn_limpiar = ttk.Button(self.header, text="🗑️ Limpiar", style="Danger.TButton", command=self.limpiar_editor)
        self.btn_limpiar.pack(side=tk.RIGHT, padx=5)

        self.btn_parse = tk.Button(self.header, text="🚀 ANALIZAR Y GENERAR DASHBOARD", bg=self.colores["btn_analizar"], fg="white", font=("Arial", 10, "bold"), borderwidth=0, padx=10, pady=5, command=self.ejecutar_analisis)
        self.btn_parse.pack(side=tk.RIGHT, padx=10)

        self.btn_cargar_archivo = tk.Button(self.header, text="📁 CARGAR ARCHIVO", bg=self.colores["btn_cargar"], fg="white", font=("Arial", 10, "bold"), borderwidth=0, padx=10, pady=5, command=self.seleccionar_archivo)
        self.btn_cargar_archivo.pack(side=tk.RIGHT, padx=5)

        # 2. CONTENEDOR EDITOR Y PREVIEW (Con etiquetas del compañero)
        self.main_container = tk.Frame(self.root, bg=self.colores["border"])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        # Columna Izquierda
        frame_izq = tk.Frame(self.main_container)
        frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(frame_izq, text="Editor de Código Smart-Home", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.editor = ScrolledText(frame_izq, font=("Consolas", 12), borderwidth=0)
        self.editor.pack(fill=tk.BOTH, expand=True, pady=2)
        self.editor.insert(tk.END, "Ingrese las instrucciones")

        # Columna Derecha
        frame_der = tk.Frame(self.main_container)
        frame_der.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Label(frame_der, text="Log de Errores Semánticos / Sintácticos / HTML", font=("Arial", 10, "bold"), fg="#c0392b").pack(anchor=tk.W)
        self.preview = ScrolledText(frame_der, font=("Consolas", 12), borderwidth=0, bg="#f9f9f9")
        self.preview.pack(fill=tk.BOTH, expand=True, pady=2)
    
    def seleccionar_archivo(self):
        ruta_archivo = filedialog.askopenfilename(
            parent=self.root,
            title="Seleccionar archivo de código Smart-Home",
            filetypes=[("SmartHome", "*.smart"), ("Todos los archivos", ".*")]
        )
        if ruta_archivo:
            self.ruta_archivo_actual = ruta_archivo
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as file:
                    instrucciones = file.read()
                self.editor.delete("1.0", tk.END)
                self.editor.insert(tk.END, instrucciones)
                self.preview.delete("1.0", tk.END)
                messagebox.showinfo("Éxito", f"Archivo cargado: {os.path.basename(ruta_archivo)}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
    
    def limpiar_editor(self):
        self.editor.delete("1.0", tk.END)
        self.preview.delete("1.0", tk.END)
        self.ruta_archivo_actual = None
    
    def ejecutar_analisis(self):
        codigo = self.editor.get("1.0", tk.END).strip()
        self.preview.delete("1.0", tk.END)
        self.compilador._lexer_obj.errores = [] 
        
        if not codigo:
            messagebox.showwarning("Atención", "El editor está vacío.")
            return

        ast = self.compilador.analizar(codigo)

        errores_lexicos = self.compilador._lexer_obj.errores
        errores_sintacticos = self.compilador.errores
        
        if errores_lexicos or errores_sintacticos:
            self.preview.insert(tk.END, "❌ SE ENCONTRARON ERRORES:\n\n")
            for err in errores_lexicos:
                self.preview.insert(tk.END, f"{err}\n")
            for err in errores_sintacticos:
                self.preview.insert(tk.END, f"Error Sintactico en L{err[0]}: Token '{err[2]}' inesperado.\n")
            
            messagebox.showerror("Error", "Se detectaron errores semánticos o sintácticos (ver log).")
        else:
            self.preview.insert(tk.END, "✅ Análisis exitoso. Generando Dashboard HTML...\n")
            html_generado = self.generar_html_desde_ast(ast)
            self.guardar_html(html_generado)
    
    def generar_html_desde_ast(self, ast):
        if not ast or ast[0] != 'PROGRAMA_HOME':
            return ""

        html = [
            "<!DOCTYPE html>",
            "<html lang='es'>",
            "<head>",
            "  <meta charset='UTF-8'>",
            "  <title>Dashboard Smart-Home</title>",
            "</head>",
            "<body style='font-family:Arial; padding:20px;'>",
            "  <h1 style='text-align:center;'>🏠 SMART-HOME</h1>" # Título del compañero
        ]

        html_body = self.recorrer_ast(ast[1])
        html.append(html_body)

        html.append("</body>\n</html>")
        return "\n".join(html)

    def recorrer_ast(self, nodo):
        if not nodo: return ""
        
        if isinstance(nodo, list):
            return "\n".join(self.recorrer_ast(n) for n in nodo)
            
        if not isinstance(nodo, tuple): return ""

        tipo = nodo[0]
        html_salida = ""

        if tipo in ('BLOQUE_CUANDO', 'BLOQUE_CADA'):
            html_salida += self.recorrer_ast(nodo[1]) 
            html_salida += self.recorrer_ast(nodo[2]) 
        elif tipo == 'CONDICIONAL':
            html_salida += self.recorrer_ast(nodo[1])
            html_salida += self.recorrer_ast(nodo[2])
            if len(nodo) > 3 and nodo[3]:
                html_salida += self.recorrer_ast(nodo[3])
        elif tipo in ('AND', 'OR', 'NOT'):
            html_salida += self.recorrer_ast(nodo[1])
            if len(nodo) > 2:
                html_salida += self.recorrer_ast(nodo[2])

        # SENSORES
        elif tipo.startswith('COMP_'):
            if len(nodo) == 5:
                sensor = f"{nodo[1]}.{nodo[2]}"
                operador = htmlutils.escape(str(nodo[3]))
                valor = htmlutils.escape(str(nodo[4]))
            elif len(nodo) == 4:
                if isinstance(nodo[1], tuple) and nodo[1][0] == 'ATTR':
                    sensor = f"{nodo[1][1]}.{nodo[1][2]}"
                else:
                    sensor = str(nodo[1])
                operador = htmlutils.escape(str(nodo[2]))
                valor = htmlutils.escape(str(nodo[3]))
            else:
                return "" 

            html_salida += f'  <div style="border: 1px solid green; padding: 20px; margin-bottom: 10px;">\n'
            html_salida += f'    <span>{sensor}</span>: {operador} {valor}\n'
            html_salida += f'  </div>\n'

        # ACTUADORES
        elif tipo.startswith('ASIG_'): 
            id_actuador = str(nodo[1])
            nombre_usuario = "" # Variable extra para el email
            
            if tipo == 'ASIG_ESTADO':
                atributo = str(nodo[2])
                valor = str(nodo[3])
            elif tipo == 'ASIG_EMAIL_NOTIF':
                atributo = 'email_notif'
                valor = str(nodo[2])
                nombre_usuario = valor.split('@')[0] # Lógica del compañero
            else:
                atributo = tipo.replace('ASIG_', '').lower()
                valor = str(nodo[2])

            html_salida += f'  <div style="border: 1px solid gray; padding: 20px; margin-bottom: 10px; border-radius: 5px;">\n'
            html_salida += f'    <h2>Dispositivo: {id_actuador}</h2>\n'
            html_salida += f'    <ul>\n'
            
            if tipo == 'ASIG_EMAIL_NOTIF':
                html_salida += f'      <li>{atributo}: <a href="mailto:{valor}">Contactar a {nombre_usuario}</a></li>\n'
            else:
                html_salida += f'      <li>{atributo}: {valor}</li>\n'
            
            html_salida += f'    </ul>\n'
            html_salida += f'  </div>\n'

        return html_salida
    
    def guardar_html(self, html_content):
        if not self.ruta_archivo_actual:
            ruta = filedialog.asksaveasfilename(
                defaultextension=".html",
                filetypes=[("HTML files", "*.html")],
                title="Guardar archivo HTML generado"
            )
            if not ruta: return
            self.ruta_archivo_actual = ruta

        output_path = os.path.splitext(self.ruta_archivo_actual)[0] + ".html"
        
        try:
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(html_content)
            
            self.preview.insert(tk.END, f"\n📁 ¡Dashboard HTML guardado con éxito en:\n{output_path}\n\n")
            self.preview.insert(tk.END, "="*40 + "\n")
            self.preview.insert(tk.END, "CÓDIGO HTML GENERADO:\n")
            self.preview.insert(tk.END, "="*40 + "\n\n")
            self.preview.insert(tk.END, html_content)
            messagebox.showinfo("Éxito", "Análisis finalizado sin errores. Dashboard generado correctamente.")

        except IOError as e:
            # Captura de error del compañero si el archivo está abierto en el navegador
            error_msg = f"Error de Sistema: No se pudo escribir '{os.path.basename(output_path)}'. Asegúrese de que no esté abierto en el navegador. ({e})"
            self.preview.insert(tk.END, f"\n❌ {error_msg}")
            messagebox.showerror("Error de E/S", error_msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = ParserInterfaz(root)
    root.mainloop()