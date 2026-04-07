# ParsingCoders

Proyecto integrador de la materia **Sintaxis y Semántica de los Lenguajes**.

---

## 🚀 ¿De qué trata?

Este proyecto busca simular el proceso básico de un compilador:

Gramática -> Lexer -> Parser


La idea es poder tomar una entrada, analizarla y verificar si cumple con una gramática definida.

---

## 🖥️ Interfaz actual

Actualmente ya contamos con una interfaz para el **analizador léxico (lexer)**:

![Interfaz](./img/interfaz.png)

> ⚠️ Nota: por ahora solo está la interfaz, el lexer todavía está en desarrollo.

---

## ⚙️ Estado del proyecto

- 🟡 Gramática → en proceso  
- 🟡 Lexer → interfaz lista, lógica en desarrollo  
- 🔴 Parser → pendiente  
- 🔴 Integración → pendiente  

---

## 🧩 ¿Qué se puede hacer por ahora?

- Ingresar texto manualmente  
- Leer archivos  
- Preparar la entrada para el análisis  

---

## 👨‍💻 Integrantes

- Elgani Fleureau, Gabriel
- Ortiz, Benito de Jesus 
- Gomez Sanches, Gabriel Nicolas
- Ruiz Diaz, Dario Nahuel 
- Bermejo, Gaston Alejandro



---

## 🛠️ Tecnologías

- Python  
- Consola  
- Manejo de archivos  

---

## ▶️ Cómo ejecutar

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
python main.py
```
Entorno virtual (venv)
Desde la carpeta del proyecto (donde está main.py):

Windows (PowerShell):
```
python -m venv venv
.\venv\Scripts\Activate.ps1
```
Windows (cmd):
```
python -m venv venv
venv\Scripts\activate.bat
```
Instalar dependencias (si tenés requirements.txt):
```
pip install -r requirements.txt
pip install pyinstaller
```
Para salir del entorno: deactivate.

Crear el ejecutable (PyInstaller)
Con el venv activado y estando en la carpeta del proyecto:
```
pyinstaller --clean main.spec
(Si no usás .spec: pyinstaller --onefile main.py y ajustá nombre/icono según necesites.)
```
Dónde queda el .exe
Por defecto PyInstaller genera:

Carpeta	Contenido
* dist/
  El ejecutable final (p. ej. dist\main.exe) — este es el que distribuís o probás.
* build/
  Archivos temporales del empaquetado — no hace falta guardarlos en Git.

