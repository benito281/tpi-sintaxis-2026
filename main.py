import os
import platform
import tkinter as tk
from colorama import Fore, init
from tkinter import filedialog
from interfaz import *

class Ejecutable:
    def __init__(self):
        self.menu_de_opciones() # Ejecuta ni bien se instancia la clase
        init() # Ayuda a camb
        
    # Limpia la pantalla ni bien se la llame
    def limpiar_pantalla(self):
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')

    # Ayuda a ingresar los datos o el código por teclado
    def leer_datos_por_teclado(self):
        print(Fore.GREEN + INSTRUCCIONES) # Muestra el menu de instrucciones por teclado
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
            print(Fore.GREEN+BANNER_PRINCIPAL) #Muestra la interfaz de las opciones
            try:
                entrada = input("Ingrese un numero para realizar una accion.\n")
                opcion = int(entrada)

                if (opcion == 1):
                    self.limpiar_pantalla()
                    codigo_final = self.leer_datos_por_teclado()       # Guardamos lo que el usuario ingreso
                    
                    print("\n--- Código capturado con éxito ---")
                    print(codigo_final) 
                    input("\nPresione Enter para volver al menú principal...")

                elif (opcion == 2):
                    print("\nIngresar ubicación de archivo")
                    self.leer_archivo()
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
            filetypes=[("Textos", "*.txt"), ("Todos", "*.*")]
        )
        root.destroy()
        print(ruta_archivo)

if __name__ == '__main__':
    ejecutar = Ejecutable()
