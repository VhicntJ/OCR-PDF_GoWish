# OCR-PDF_GoWish

# Proyecto Go Wish en Cuidado Paliativo

## Descripción del Proyecto

Este proyecto busca aplicar inteligencia artificial y reconocimiento óptico de caracteres (OCR) para mejorar el uso de las cartas Go Wish en el contexto de cuidados paliativos en centros de salud. Las cartas Go Wish ayudan a los pacientes a expresar sus deseos y prioridades en situaciones de cuidados paliativos. Nuestra solución automatiza la generación de datos estadísticos a partir de las cartas seleccionadas por los pacientes.

## Integrantes del Equipo

- Vicente Julio
- Rony Perez
- Ignacio Vera
- Matias Auriol

## Profesor Guía

- Patricio Rojas Carrasco

## Colaboración

Trabajamos en conjunto con el profesor Álvaro Leyton Hernández de enfermería que nos guió en la comprensión y aplicación de las cartas Go Wish en el cuidado paliativo.

## Objetivo

Desarrollar una solución que, a través de inteligencia artificial y OCR, analice los PDFs generados por la página web de Go Wish y extraiga los caracteres de cada tarjeta seleccionada por el paciente. Esto nos permite:
1. Obtener información detallada sobre las preferencias del paciente.
2. Asignar formularios personalizados al paciente con los datos necesarios para un muestreo estadístico.
3. Guardar toda la información en una base de datos para análisis posteriores.

## Tecnologías Utilizadas

- Python
- Librerías:
  - `pdf2image`
  - `pytesseract`
  - `PIL` (Python Imaging Library)
  - `tkinter`
  - `sqlite3`
  - `uuid`
  - `difflib`

## Funcionalidades del Código

1. **Conversión de PDF a Imagen**: Utiliza la librería `pdf2image` para convertir archivos PDF en imágenes.
2. **Reconocimiento de Caracteres (OCR)**: Usa `pytesseract` para extraer texto de las imágenes.
3. **Interfaz Gráfica**: Implementa una interfaz gráfica con `tkinter` para facilitar la interacción del usuario.
4. **Base de Datos**: Almacena la información extraída en una base de datos SQLite.
5. **Comparación de Textos**: Utiliza `difflib` para encontrar coincidencias cercanas entre los textos extraídos y las posibles opciones de las cartas Go Wish.
6. **Creación y Población de la Base de Datos**: Crea las tablas necesarias en la base de datos y las llena con las cartas Go Wish.
7. **Selección de Archivos**: Permite al usuario seleccionar archivos PDF a procesar.
8. **Procesamiento de PDF**: Convierte páginas de PDF a imágenes, recorta y procesa partes específicas para extraer el texto deseado.
9. **Almacenamiento y Visualización de Resultados**: Guarda los resultados en una base de datos y en un archivo de texto, además de mostrarlos en una ventana de resultados.

## Estructura del Proyecto

- `main.py`: Script principal que coordina el flujo del programa.
- `ocr.py`: Módulo encargado de la conversión de PDF a imagen y el reconocimiento de caracteres.
- `gui.py`: Módulo que gestiona la interfaz gráfica del usuario.
- `database.py`: Módulo que maneja la interacción con la base de datos SQLite.
- `utils.py`: Funciones utilitarias para el procesamiento de texto y datos.

