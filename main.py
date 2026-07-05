import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import html as htmlutils
import os
from parser import SmartHomeParser

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TPI UTN FRRE - Smart-Home System - ParsingCoders")
        self.geometry("850x700") 
        
        self.ruta_archivo_actual = None
        self.compilador = SmartHomeParser()
        
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Frame para botones superiores
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        # Botones de Acción
        tk.Button(btn_frame, text="📁 CARGAR ARCHIVO", bg="#2980b9", fg="white", 
                  font=("Arial", 10, "bold"), command=self.cargar_archivo).pack(side=tk.LEFT, padx=10)
        # Parsear
        tk.Button(btn_frame, text="🚀 ANALIZAR Y GENERAR DASHBOARD", bg="#d35400", fg="white", 
                  font=("Arial", 10, "bold"), command=self.run).pack(side=tk.LEFT, padx=10)

        # Limpiar
        tk.Button(btn_frame, text="🗑️ LIMPIAR", bg="#e74c3c", fg="white", 
                  font=("Arial", 10, "bold"), command=self.limpiar).pack(side=tk.LEFT, padx=10)

        # Editor de instrucciones
        tk.Label(self, text="Editor de Código Smart-Home", font=("Arial", 10, "bold")).pack()
        self.editor = scrolledtext.ScrolledText(self, width=95, height=20, font=("Consolas", 11))
        self.editor.pack(pady=5)
        
        # Log de errores
        tk.Label(self, text="Log de Errores / Resultados", font=("Arial", 10, "bold"), fg="#c0392b").pack()
        self.log = scrolledtext.ScrolledText(self, width=95, height=10, fg="#c0392b", bg="#f9f9f9", font=("Consolas", 10))
        self.log.pack(pady=5)

    #Limpia el editor y la consola
    def limpiar(self):
        self.editor.delete(1.0, tk.END)
        self.log.delete(1.0, tk.END)
        self.log.configure(fg="#c0392b") # Restaurar color rojo por defecto
        self.ruta_archivo_actual = None
        self.compilador._lexer_obj.errores.clear()

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de código Smart-Home",
            filetypes=(("Archivos Smart", "*.smart"), ("Todos los archivos", ".*"))
        )
        if ruta:
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read()
                    self.editor.delete(1.0, tk.END)
                    self.editor.insert(tk.END, contenido)
                self.ruta_archivo_actual = ruta
                messagebox.showinfo("Éxito", f"Archivo cargado: {os.path.basename(ruta)}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

    def run(self):
        # Limpieza de log y lexer
        self.log.delete(1.0, tk.END)
        self.log.configure(fg="#c0392b") 
        self.compilador._lexer_obj.errores.clear()
        
        entrada = self.editor.get(1.0, tk.END).strip()
        if not entrada:
            messagebox.showwarning("Atención", "El editor está vacío.")
            return

        # Ejecuta el analisis en una pasada
        html_generado = self.compilador.analizar(entrada)

        errores_lex = self.compilador._lexer_obj.errores
        errores_sin = self.compilador.errores

        if errores_lex or errores_sin:
            for err in errores_lex:
                self.log.insert(tk.END, f"❌ [LÉXICO] {err}\n")
            for err in errores_sin:
                self.log.insert(tk.END, f"❌ [SINTÁCTICO] Error en L{err[0]}: Token '{err[2]}' inesperado.\n")
            messagebox.showerror("Error", "Se detectaron errores semánticos o sintácticos (ver log).")
        else:
            self.log.configure(fg="#27ae60") 
            self.log.insert(tk.END, "✅ Análisis exitoso. Generando Dashboard HTML...\n")
            
            # Se guarda el string devuelto por el parser
            self.guardar_html(html_generado)

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
            
            self.log.insert(tk.END, f"📁 ¡Dashboard HTML guardado con éxito en:\n{output_path}\n")
            messagebox.showinfo("Éxito", "Análisis finalizado sin errores. Dashboard generado correctamente.")

        except IOError as e:
            error_msg = f"Error de Sistema: No se pudo escribir '{os.path.basename(output_path)}'. Asegúrese de que no esté abierto en el navegador. ({e})"
            self.log.configure(fg="#c0392b")
            self.log.insert(tk.END, f"\n❌ {error_msg}")
            messagebox.showerror("Error de E/S", error_msg)

if __name__ == "__main__":
    app = App()
    app.mainloop()