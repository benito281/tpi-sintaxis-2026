import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import html as htmlutils
import os
from parser import SmartHomeParser

class ParserInterfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("ParsingCoders")
        self.root.geometry("1100x700")
        self.ruta_archivo_actual = None
        self.compilador = SmartHomeParser()
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
        #Header
        self.header = ttk.Frame(self.root, style="Header.TFrame", padding=15)
        self.header.pack(fill=tk.X)
        #Botones
        self.btn_cargar_archivo = ttk.Button(self.header, text="📂Cargar archivo", style="Invert.TButton", command=self.seleccionar_archivo)
        self.btn_cargar_archivo.pack(side=tk.RIGHT, padx=5)

        self.btn_parse = ttk.Button(self.header, text="🌐Parsear a HTML ", style="Primary.TButton", command=self.ejecutar_analisis)
        self.btn_parse.pack(side=tk.RIGHT, padx=5)

        self.btn_limpiar = ttk.Button(self.header, text="🗑️Limpiar ", style="Danger.TButton", command=self.limpiar_editor)
        self.btn_limpiar.pack(side=tk.RIGHT, padx=5)
        #Tiulo
        self.nombre = ttk.Label(self.header, text="SmartHome", style="Header.TLabel")
        self.nombre.pack(side=tk.LEFT, padx=5)


        #Editor y preview
        self.main_container = tk.Frame(self.root, bg=self.colores["border"])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        # 
        self.editor = ScrolledText(self.main_container, font=("Segoe UI", 12), borderwidth=0)
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.editor.insert(tk.END,"Ingrese las instrucciones")

        self.preview = ScrolledText(self.main_container, font=("Segoe UI", 12), borderwidth=0)
        self.preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    #Busqueda y selección de archivo
    def seleccionar_archivo(self):
        ruta_archivo = filedialog.askopenfilename(
            parent=self.root,
            title="Elija un archivo",
            filetypes=[("SmartHome", "*.smart")]
        )
        if ruta_archivo:
            self.ruta_archivo_actual = ruta_archivo
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as file:
                    instrucciones = file.read()
                self.editor.delete("1.0", tk.END)
                self.editor.insert(tk.END, instrucciones)
                self.preview.delete("1.0", tk.END)
            except FileNotFoundError:
                messagebox.showerror("Error", "No se encontró el archivo seleccionado.")
            except PermissionError:
                messagebox.showerror("Error", "No tenés permiso para abrir ese archivo.")
            except OSError as error:
                messagebox.showerror("Error", f"No se pudo abrir el archivo: {error}")
    #Limpia el contenido de la pantalla
    def limpiar_editor(self):
        self.editor.delete("1.0", tk.END)
        self.preview.delete("1.0", tk.END)
        self.ruta_archivo_actual = None
    
    def ejecutar_analisis(self):
        #Limpiar errores previos y consolas
        codigo = self.editor.get("1.0", tk.END).strip()
        self.preview.delete("1.0", tk.END)
        self.compilador._lexer_obj.errores = [] 
        
        if not codigo:
            messagebox.showwarning("Advertencia", "El editor está vacío.")
            return

        #Ejecutar el parser 
        ast = self.compilador.analizar(codigo)

        #Recopilar todos los errores (Léxicos + Sintácticos)
        errores_lexicos = self.compilador._lexer_obj.errores
        errores_sintacticos = self.compilador.errores
        
        if errores_lexicos or errores_sintacticos:
            # Mostrar errores
            self.preview.insert(tk.END, "❌ SE ENCONTRARON ERRORES:\n\n")
            for err in errores_lexicos:
                self.preview.insert(tk.END, f"LÉXICO: {err}\n")
            for err in errores_sintacticos:
                self.preview.insert(tk.END, f"SINTÁCTICO: Error en línea {err[0]}: token inesperado '{err[2]}'\n")
            
            messagebox.showerror("Error", "El código contiene errores. Revisa el panel derecho.")
        else:
            #Mensaje de exito
            self.preview.insert(tk.END, "✅ Análisis exitoso. Generando HTML...\n")
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
            "  <title>Reporte de Ejecución SmartHome</title>",
            "<script src='https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4'></script>",
            "</head>",
            "<body>",
            "  <h1>Reporte de Configuración - SmartHome</h1>"
        ]

        # Desatar la recursión a partir del nivel 1 (lista_instrucciones)
        html_body = self.recorrer_ast(ast[1])
        html.append(html_body)

        html.append("</body>\n</html>")
        return "\n".join(html)

    def recorrer_ast(self, nodo):
        """
        Recorre recursivamente los nodos del AST para procesar instrucciones anidadas
        y aplica el HTML correspondiente según el tipo de nodo.
        """
        if not nodo: return ""
        
        # Si es una lista, se recorre cada instrucción internamente
        if isinstance(nodo, list):
            return "\n".join(self.recorrer_ast(n) for n in nodo)
            
        if not isinstance(nodo, tuple): return ""

        tipo = nodo[0]
        html_salida = ""

        # BLOQUES ANIDADOS (IF, WHEN, EVERY)
        # Evaluamos hijos pero no generamos HTML visible extra para ellos
        # (salvo que desees agregar identificadores de bloque en un futuro)
        if tipo in ('BLOQUE_CUANDO', 'BLOQUE_CADA'):
            html_salida += self.recorrer_ast(nodo[1]) 
            html_salida += self.recorrer_ast(nodo[2]) 
        elif tipo == 'CONDICIONAL':
            html_salida += self.recorrer_ast(nodo[1])
            html_salida += self.recorrer_ast(nodo[2])
            if len(nodo) > 3 and nodo[3]: # ELSE
                html_salida += self.recorrer_ast(nodo[3])
        elif tipo in ('AND', 'OR', 'NOT'):
            html_salida += self.recorrer_ast(nodo[1])
            if len(nodo) > 2:
                html_salida += self.recorrer_ast(nodo[2])

        # -----------------------------------------------------
        # SENSORES
        # div con borde 1px verde, padding 20px. Nombre en <span>.
        # -----------------------------------------------------
        elif tipo.startswith('COMP_'):
            sensor = str(nodo[1])
            if isinstance(nodo[1], tuple):
                sensor = f"{nodo[1][1]}.{nodo[1][2]}"
                
            operador = htmlutils.escape(str(nodo[2])) if len(nodo) > 2 else ""
            valor = htmlutils.escape(str(nodo[3])) if len(nodo) > 3 else ""

            html_salida += f'  <div style="border: 1px solid green; padding: 20px; margin-bottom: 10px;">\n'
            html_salida += f'    <span>{sensor}</span>: {operador} {valor}\n'
            html_salida += f'  </div>\n'

        # -----------------------------------------------------
        # ACTUADORES
        # div con borde 1px gris, padding 20px. Nombre en <h3>.
        # Atributos en <ul><li>, Mails en <a>.
        # -----------------------------------------------------
        elif tipo.startswith('ASIG_'): 
            id_actuador = str(nodo[1])
            
            if tipo == 'ASIG_ESTADO':
                atributo = str(nodo[2])
                valor = str(nodo[3])
            elif tipo == 'ASIG_EMAIL_NOTIF':
                atributo = 'email_notif'
                valor = str(nodo[2])
            else:
                atributo = tipo.replace('ASIG_', '').lower()
                valor = str(nodo[2])

            html_salida += f'  <div style="border: 1px solid gray; padding: 20px; margin-bottom: 10px;">\n'
            html_salida += f'    <h3>{id_actuador}</h3>\n'
            html_salida += f'    <ul>\n'
            
            if tipo == 'ASIG_EMAIL_NOTIF':
                html_salida += f'      <li>{atributo}: <a href="mailto:{valor}">Contactar a {valor}</a></li>\n'
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

        # Cambio de extensión a .html
        output_path = os.path.splitext(self.ruta_archivo_actual)[0] + ".html"
        
        try:
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(html_content)
            
            # Imprimir resultado y HTML en el preview
            self.preview.insert(tk.END, f"\n📁 ¡Archivo HTML guardado con éxito en:\n{output_path}\n\n")
            self.preview.insert(tk.END, "="*40 + "\n")
            self.preview.insert(tk.END, "CÓDIGO HTML GENERADO:\n")
            self.preview.insert(tk.END, "="*40 + "\n\n")
            self.preview.insert(tk.END, html_content)

        except Exception as e:
            self.preview.insert(tk.END, f"\n❌ Error al guardar el archivo: {e}")
            messagebox.showerror("Error de E/S", f"No se pudo guardar el HTML:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ParserInterfaz(root)
    root.mainloop()