import os
import platform
import tkinter as tk
from tkinter import filedialog
from interfaz import *
from lexer import LexerTokens as tokens

lexer = tokens() # Instancia de la clase LexerTokens
lexer.build() # Construye el lexer


class Ejecutable:
    def __init__(self):
        self.menu_de_opciones() # Ejecuta ni bien se instancia la clase
        
    # Limpia la pantalla ni bien se la llame
    def limpiar_pantalla(self):
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')

    # Ayuda a ingresar los datos o el código por teclado
    def leer_datos_por_teclado(self):
        print(INSTRUCCIONES) # Muestra el menu de instrucciones por teclado
        lineas = []
        try:
            while True:
                linea = input("Línea: ")
                lineas.append(linea)
        
        except EOFError:
            print("\n")
            return '\n'.join(lineas)

    # Menu basico e interactivo
    def menu_de_opciones(self):
        while True:
            self.limpiar_pantalla()
            print(BANNER_PRINCIPAL) #Muestra la interfaz de las opciones
            try:
                print("Ingrese un numero para realizar una accion.")
                entrada = input()
                opcion = int(entrada)
                if (opcion == 1):
                    self.limpiar_pantalla()
                    codigo_final = self.leer_datos_por_teclado()       # Guardamos lo que el usuario ingreso
                    lexer.test(codigo_final)
                    input("\nPresione Enter para volver al menú principal...")

                elif (opcion == 2):
                    print("\nIngresar ubicación de archivo")
                    nombre_ubicacion = self.leer_archivo()
                    if nombre_ubicacion:
                        # Abrimos el archivo y leemos su contenido
                        with open(nombre_ubicacion, 'r', encoding='utf-8') as archivo:
                            codigo_archivo = archivo.read()
                        
                        lexer.test(codigo_archivo)
                        input("\nPresione Enter para volver al menú principal...")
                    else:
                        print("No se introdujo el nombre de ningún archivo o este no existe.")
                        input("\nPresione Enter para volver al menú principal...")

                elif (opcion == 3):
                    self.limpiar_pantalla()
                    print("\nSaliendo...")
                    break
                else:
                    self.limpiar_pantalla()
                    print("⚠️ Opción no válida. Por favor, ingrese 1, 2 o 3.\n")
                    input("Presione Enter para volver al menú principal...")



            except EOFError:
                print("\nCaracter de fin de archivo ingresado. Saliendo del programa.")
            except FileNotFoundError:
               print("\n Archivo no encontrado.")

    def leer_archivo(self):
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        root.update()
        ruta_archivo = filedialog.askopenfilename(
            parent=root,
            title="Elija un archivo",
            filetypes=[("SmartHome", "*.smart"),("Textos", "*.txt")]
        )
        root.destroy()
        print(ruta_archivo)
        return ruta_archivo

if __name__ == '__main__':
    ejecutar = Ejecutable()
