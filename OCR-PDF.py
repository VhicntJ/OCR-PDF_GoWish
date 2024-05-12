from pdf2image import convert_from_path
import img2pdf
import pytesseract
from PIL import Image
import glob
import os

# Directorio donde se encuentran los archivos PDF
pdf_directory = "pdfs/"

# Directorio donde se guardarán las imágenes originales
original_image_directory = "original_images/"

# Directorio donde se guardarán las imágenes procesadas
processed_image_directory = "processed_images/"

# Directorio donde se guardarán las imágenes temporales
temp_image_directory = "temp_images/"

# Directorio donde se guardarán los archivos de texto de la primera categoría
output_directory_cat1 = "text_files_categoria1/"

# Directorio donde se guardarán los archivos de texto de la segunda categoría
output_directory_cat2 = "text_files_categoria2/"

# Crear los directorios si no existen
os.makedirs(original_image_directory, exist_ok=True)
os.makedirs(processed_image_directory, exist_ok=True)
os.makedirs(temp_image_directory, exist_ok=True)
os.makedirs(output_directory_cat1, exist_ok=True)
os.makedirs(output_directory_cat2, exist_ok=True)

# Obtener la lista de archivos PDF en el directorio
pdfs = glob.glob(pdf_directory + "*.pdf")

# Configurar la resolución de conversión de PDF a imagen
pdf_resolution = 600  # Puedes ajustar esto según tu preferencia

# Configurar el idioma para el OCR
language = 'spa'

# Define las coordenadas de los 11 cuadros (x, y, width, height) para la primera categoría
cuadros_cat1 = [
    (20, 25, 471, 508),
    (600, 41, 355, 494),
    (1039, 41, 355, 494),
    (1467, 34, 355, 494),
    (1897, 41, 355, 494),
    (2334, 41, 355, 494),
    (2764, 41, 355, 494),
    (3201, 41, 355, 494),
    (3645, 41, 355, 494),
    (4075, 41, 355, 494),
    (4505, 41, 355, 494),
    # Agrega las coordenadas de los demás cuadros aquí
]

# Define las coordenadas de los 11 cuadros (x, y, width, height) para la segunda categoría
cuadros_cat2 = [
    (34, 50, 459, 437),
    (609, 55, 355, 494),
    (1047, 55, 355, 494),
    (1465, 55, 355, 494),
    (1910, 55, 355, 494),
    (2341, 55, 355, 494),
    (2780, 55, 355, 494),
    (3211, 55, 355, 494),
    (3642, 55, 355, 494),
    (4073, 55, 355, 494),
    (4504, 55, 355, 494),
    (612, 649, 355, 494),
    (1051, 649, 355, 494),
    (1482, 649, 355, 494),
    (1913, 649, 355, 494),
    (2344, 649, 355, 494),
    (2775, 649, 355, 494),
    (3206, 649, 355, 494),
    (3645, 649, 355, 494),
    (4076, 649, 355, 494),
    (4498, 649, 355, 494),
    
    # Agrega las coordenadas de los demás cuadros aquí
]

# Procesar cada archivo PDF
for pdf_path in pdfs:
    try:
        # Convertir el PDF a imágenes
        pages = convert_from_path(pdf_path, dpi=pdf_resolution)

        # Guardar las imágenes originales
        for pageNum, imgBlob in enumerate(pages):
            original_image_path = os.path.join(original_image_directory, f"{os.path.basename(pdf_path)[:-4]}_original_page_{pageNum}.jpg")
            imgBlob.save(original_image_path, "JPEG")

        # Procesar cada página
        for pageNum, imgBlob in enumerate(pages):
            # Guardar la imagen temporal
            temp_image_path = os.path.join(temp_image_directory, f"temp_page_{pageNum}.jpg")
            imgBlob.save(temp_image_path, "JPEG")

            # Abrir la imagen recién guardada
            img = Image.open(temp_image_path)

            # Recortar la parte superior (1268 píxeles) y la parte inferior (2069 píxeles) de la imagen
            width, height = img.size
            cropped_img = img.crop((0, 1268, width, height - 2069))

            # Guardar la imagen recortada
            processed_image_path = os.path.join(processed_image_directory, f"{os.path.basename(pdf_path)[:-4]}_processed_page_{pageNum}.jpg")
            cropped_img.save(processed_image_path, "JPEG")

            # Recortar las dos categorías adicionales
            # Categoria 1: imagen sector superior
            cat1_img = cropped_img.crop((98, 45, 98 + 4914, 45 + 592))
            cat1_img_path = os.path.join(processed_image_directory, f"{os.path.basename(pdf_path)[:-4]}_cat1_page_{pageNum}.jpg")
            cat1_img.save(cat1_img_path, "JPEG")

            # Categoria 2: imagen sector inferior
            cat2_img = cropped_img.crop((89, 2066, 89 + 4932, 2066 + 1188))
            cat2_img_path = os.path.join(processed_image_directory, f"{os.path.basename(pdf_path)[:-4]}_cat2_page_{pageNum}.jpg")
            cat2_img.save(cat2_img_path, "JPEG")

            # Procesar cada imagen con OCR y guardar el texto extraído en archivos de texto
            for cat_img, output_dir, cuadros in [(cat1_img, output_directory_cat1, cuadros_cat1), (cat2_img, output_directory_cat2, cuadros_cat2)]:
                # Inicializa una lista para almacenar el texto de cada cuadro
                texto_cuadros = []

                # Itera sobre las coordenadas de los cuadros
                for i, (x, y, width, height) in enumerate(cuadros):
                    # Recorta el cuadro actual de la imagen
                    cuadro_img = cat_img.crop((x, y, x + width, y + height))

                    # Extrae texto del cuadro con OCR
                    texto = pytesseract.image_to_string(cuadro_img, lang=language)

                    # Agrega el texto al texto de cuadros
                    texto_cuadros.append(f"Carta {i+1}: {texto}")

                # Combina el texto de los cuadros en un solo texto
                texto_final = "\n".join(texto_cuadros)

                # Guarda el texto en el archivo de texto correspondiente
                output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(cat2_img_path))[0]}_page_{pageNum}.txt")
                with open(output_file, 'w', encoding='utf-8') as the_file:
                    the_file.write(texto_final)

    except Exception as e:
        print(f"Error al procesar {pdf_path}: {e}")

# Eliminar las imágenes temporales
for file in os.listdir(temp_image_directory):
    file_path = os.path.join(temp_image_directory, file)
    if os.path.isfile(file_path):
        os.remove(file_path)
