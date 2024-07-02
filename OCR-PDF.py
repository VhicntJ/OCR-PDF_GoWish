from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import sqlite3
import uuid
from difflib import get_close_matches
import sys

os.path.join(os.path.dirname(sys.executable), 'Scripts')
os.path.dirname(sys.executable)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR'

# Diccionario de cartas con sus IDs
cartas = {
    "A1": "Morir en mi casa",
    "A2": "Atender asuntos inconclusos con mi familia y amigos",
    "A3": "Ser tratado de la manera que yo quiero",
    "A4": "Estar sin ansiedad",
    "A5": "Poder quedarme en mi casa",
    "A6": "Mantener mi sentido del humor",
    "A7": "Platicar con un sacerdote,pastor,rabino,capellán,...",
    "A8": "Poder ayudar a los demás",
    "A9": "Mantener mi dignidad",
    "B1": "Tener confianza en mi doctor",
    "B2": "Que no me falte el aire",
    "B3": "Sentir que mi vida está completa",
    "B4": "Poder hablar y ser comprendido",
    "B5": "Estar consciente de lo que está pasando",
    "B6": "Tener a mi familia conmigo",
    "B7": "Que me mantengan limpio",
    "B8": "Tener a mis amistades cerca de mí",
    "B9": "Tener mis asuntos financieros en orden",
    "C1": "No estar conectado a máquinas",
    "C2": "No morir solo",
    "C3": "Tener a alguien que me escuche",
    "C4": "Asegurar que mi familia conozca mis deseos para evitar desacuerdos",
    "C5": "Despedirme de las personas importantes en mi vida",
    "C6": "Poder hablar sobre lo que significa morir",
    "C7": "Poder Reconocer a mis familiares y amistades",
    "C8": "Poder hablar sobre mis temores",
    "C9": "Que mi familia esté preparada para mi muerte",
    "D1": "Estar sin dolor",
    "D2": "Recordar logros personales",
    "D3": "Estar en paz con Dios",
    "D4": "No ser una carga para mi familia",
    "D5": "Sentir calor humano",
    "D6": "Comer y disfrutar la comida",
    "D7": "Rezar/Orar",
    "D8": "Saber qué cambios puede tener mi cuerpo",
    "D9": "CARTA LIBRE"
}
enfermedades_comunes = [
    "Enfermedades cardíacas", "Cáncer", "Enfermedades respiratorias", "Accidente cerebrovascular",
    "Enfermedades de Alzheimer", "Diabetes", "Insuficiencia renal", "Enfermedad hepática crónica",
    "Enfermedad pulmonar obstructiva crónica (EPOC)", "Neumonía", "Sepsis", "Enfermedades neurológicas",
    "Enfermedades infecciosas", "Enfermedades autoinmunes", "Enfermedades genéticas",
    "Enfermedades hematológicas", "Enfermedades metabólicas", "Enfermedades degenerativas",
    "Enfermedades gastrointestinales", "Enfermedades renales","Tuberculosis","VIH/SIDA",
"Sepsis",
"Hepatitis B y C",
"Meningitis bacteriana",
"Neumonía bacteriana",
"Infección por Clostridium difficile",
"Septicemia",
"Cáncer de pulmón",
"Cáncer de mama",
"Cáncer de próstata",
"Cáncer colorrectal",
"Cáncer de páncreas",
"Cáncer de hígado",
"Cáncer de esófago",
"Cáncer de estómago",
"Leucemia mieloide aguda",
"Leucemia linfocítica crónica",
"Linfoma de Hodgkin",
"Linfoma no Hodgkin",
"Mieloma múltiple",
"Glioblastoma",
"Leucemia aguda",
"Linfoma maligno",
"Anemia aplásica",
"Mielodisplasia",
"Anemia falciforme con crisis severas",
"Trombocitopenia severa",
"Lupus eritematoso sistémico severo",
"Esclerosis múltiple en etapa avanzada",
"Artritis reumatoide con complicaciones sistémicas",
"Enfermedad de Still del adulto",
"Enfermedad de Behçet",
"Síndrome de Sjögren con complicaciones",
"Diabetes mellitus tipo 1 con complicaciones (neuropatía, nefropatía, retinopatía)",
"Diabetes mellitus tipo 2 con complicaciones (ulceraciones, gangrena)",
"Insuficiencia suprarrenal aguda",
"Hipotiroidismo severo (coma mixedematoso)",
"Hipertiroidismo severo (tormenta tiroidea)",
"Hiperparatiroidismo con complicaciones",
"Enfermedad de Graves avanzada",
"Enfermedad de Parkinson avanzada",
"Esclerosis lateral amiotrófica (ELA)",
"Epilepsia refractaria",
"Meningitis bacteriana",
"Encefalitis viral",
"Neuropatía periférica severa",
"Accidente cerebrovascular (ACV) con secuelas graves",
"Glioblastoma multiforme",
"Infarto agudo de miocardio",
"Insuficiencia cardíaca congestiva avanzada",
"Enfermedad coronaria crítica",
"Miocardiopatía dilatada",
"Miocardiopatía hipertrófica obstructiva",
"Aneurisma aórtico roto",
"Enfermedad arterial periférica severa",
"Endocarditis infecciosa",
"Enfermedad pulmonar obstructiva crónica (EPOC) en etapa final",
"Neumonía bacteriana grave",
"Fibrosis pulmonar idiopática",
"Asma severa y resistente al tratamiento",
"Cáncer de pulmón metastásico",
"Embolia pulmonar masiva",
"Bronquiectasias con infecciones recurrentes",
"Cirrosis hepática descompensada",
"Insuficiencia hepática fulminante",
"Cáncer de hígado avanzado",
"Pancreatitis crónica con complicaciones",
"Colitis ulcerosa fulminante",
"Enfermedad de Crohn con complicaciones graves",
"Carcinoma esofágico",
"Hepatitis alcohólica severa",
"Úlceras de decúbito infectadas",
"Melanoma maligno metastásico",
"Carcinoma de células escamosas",
"Psoriasis pustulosa generalizada",
"Esclerodermia sistémica progresiva",
"Artritis reumatoide con daño articular severo",
"Lupus eritematoso sistémico con afectación renal",
"Esclerosis sistémica con afectación pulmonar",
"Polimiositis con afectación sistémica",
"Dermatomiositis con complicaciones",
"Insuficiencia renal crónica en etapa terminal",
"Cáncer renal metastásico",
"Cáncer de vejiga avanzado",
"Hiperplasia prostática benigna con complicaciones severas",
"Nefropatía diabética avanzada",
"Síndrome nefrótico con insuficiencia renal",
"Traumatismo craneoencefálico severo con deterioro neurológico",
"Lesiones medulares con cuadriplejía",
"Quemaduras extensas con complicaciones sistémicas",
"Intoxicación por sustancias tóxicas con daño orgánico múltiple",
]

# Crear la base de datos y las tablas
def crear_base_datos():
    conn = sqlite3.connect('resultados.db')
    c = conn.cursor()
    
    # Crear tabla para los datos del paciente
    c.execute('''CREATE TABLE IF NOT EXISTS pacientes (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 patient_id TEXT,
                 nombre TEXT,
                 sexo TEXT,
                 edad TEXT,
                 oficio TEXT,
                 enfermedad TEXT)''')
    
    # Crear tabla para las cartas
    c.execute('''CREATE TABLE IF NOT EXISTS cartas (
                 carta_id TEXT PRIMARY KEY,
                 descripcion TEXT)''')
    
    # Crear tabla para los resultados
    c.execute('''CREATE TABLE IF NOT EXISTS resultados (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 patient_id TEXT,
                 categoria TEXT,
                 carta_id TEXT,
                 texto TEXT,
                 FOREIGN KEY (patient_id) REFERENCES pacientes (patient_id))''')
    
    conn.commit()
    conn.close()
class AutocompleteEntry(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.suggestions = []
        self.enfermedad = tk.StringVar()  # Variable para almacenar la enfermedad seleccionada
        
        self.entry = tk.Entry(self, font=("Helvetica", 12), width=40)
        self.entry.pack(fill="x", padx=10, pady=10)
        self.entry.insert(0, "Escriba la enfermedad")
        self.entry.bind("<FocusIn>", self.clear_placeholder)
        self.entry.bind("<FocusOut>", self.restore_placeholder)
        self.entry.bind("<KeyRelease>", self.handle_keyrelease)
        
        self.listbox = tk.Listbox(self, font=("Helvetica", 12), width=40)
        self.listbox.pack(fill="both", expand=True)
        self.listbox.bind("<ButtonRelease-1>", self.fill_entry)
        self.listbox.bind("<Return>", self.fill_entry)
        
        self.hide_listbox()

    def clear_placeholder(self, event):
        if self.entry.get() == "Escriba la enfermedad":
            self.entry.delete(0, tk.END)

    def restore_placeholder(self, event):
        if not self.entry.get():
            self.entry.insert(0, "Escriba la enfermedad")

    def handle_keyrelease(self, event):
        text = self.entry.get().lower()
        self.suggestions = [item for item in enfermedades_comunes if text in item.lower()]
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for item in self.suggestions:
            self.listbox.insert(tk.END, item)
        if self.suggestions:
            self.show_listbox()
        else:
            self.hide_listbox()

    def show_listbox(self):
        self.listbox.pack()

    def hide_listbox(self):
        self.listbox.pack_forget()

    def fill_entry(self, event):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            selected_text = self.listbox.get(index)
            self.enfermedad.set(selected_text)  # Guardar la enfermedad seleccionada en la variable
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected_text)
            self.hide_listbox()
        elif event.keysym == "Return":
            self.enfermedad.set(self.entry.get())  # Guardar la enfermedad escrita manualmente en la variable
            self.hide_listbox()

# Llamar a la función para crear la base de datos y las tablas
crear_base_datos()

# Función para insertar las cartas en la base de datos
def insertar_cartas():
    conn = sqlite3.connect('resultados.db')
    c = conn.cursor()
    
    for carta_id, descripcion in cartas.items():
        c.execute('''INSERT OR IGNORE INTO cartas (carta_id, descripcion)
                     VALUES (?, ?)''', (carta_id, descripcion))
    
    conn.commit()
    conn.close()

# Llamar a la función para insertar las cartas en la base de datos
insertar_cartas()


# Función para seleccionar un archivo PDF
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
    if archivo:
        entry_archivo_pdf.delete(0, tk.END)
        entry_archivo_pdf.insert(0, archivo)

# Función para mostrar los resultados
def mostrar_resultados(texto_final):
    resultados_ventana = tk.Toplevel(root)
    resultados_ventana.title("Resultados de Texto")
    resultados_ventana.geometry("800x600")
    resultados_ventana.configure(bg="#f0f0f0")
    
    texto_resultados = scrolledtext.ScrolledText(resultados_ventana, wrap=tk.WORD, font=("Helvetica", 12), bg="#ffffff", fg="#333333")
    texto_resultados.pack(expand=True, fill='both', padx=10, pady=10)
    
    texto_resultados.insert(tk.END, texto_final)
    texto_resultados.config(state=tk.DISABLED)

# Función para guardar los resultados en un archivo de texto
def guardar_resultados(texto_final, patient_id):
    conn = sqlite3.connect('resultados.db')
    c = conn.cursor()
    # Guardar datos del paciente
    nombre = entry_nombre.get()
    sexo = combo_sexo.get()
    edad_str = entry_edad.get()
    oficio = entry_oficio.get()
    enfermedad = autocomplete_entry.enfermedad.get()

    c.execute('''INSERT INTO pacientes (patient_id, nombre, sexo, edad, oficio, enfermedad) 
                 VALUES (?, ?, ?, ?, ?, ?)''', 
              (patient_id, nombre, sexo, edad_str, oficio, enfermedad))
    
    # Procesar el texto final para guardar los resultados categorizados
    lines = texto_final.split('\n')
    categoria = None

    for line in lines:
        line = line.strip()
        if line.startswith("Desconocido: Muy"):
            categoria = "Muy Importante"
        elif line.startswith("Desconocido: Nada"):
            categoria = "Nada Importante"
        elif line and categoria:
            if ':' in line:
                carta_id, texto = line.split(':', 1)
                c.execute('''INSERT INTO resultados (patient_id, categoria, carta_id, texto)
                             VALUES (?, ?, ?, ?)''', 
                          (patient_id, categoria, carta_id.strip(), texto.strip()))
    
    conn.commit()
    conn.close()
    messagebox.showinfo("Información", f"Resultados guardados en la base de datos con ID {patient_id}")


    archivo_salida = f"resultados_{patient_id}.txt"
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(texto_final)
    messagebox.showinfo("Información", f"Resultados guardados en {archivo_salida}")



def limpiar_campos():
    entry_archivo_pdf.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    combo_sexo.set('')  # Limpiar el combobox seleccionándolo en vacío
    entry_edad.delete(0, tk.END)
    entry_oficio.delete(0, tk.END)
    autocomplete_entry.entry.delete(0, tk.END)  # Limpiar el AutocompleteEntry


    
# Función para procesar el archivo PDF
def procesar_pdf():
    pdf_path = entry_archivo_pdf.get()
    nombre = entry_nombre.get()
    sexo = combo_sexo.get()
    edad = entry_edad.get()
    oficio = entry_oficio.get()
    enfermedad = autocomplete_entry.enfermedad.get()

    if not os.path.exists(pdf_path):
        messagebox.showerror("Error", "El archivo no existe")
        return

    if not nombre or not sexo or not edad or not oficio or not enfermedad:
        messagebox.showerror("Error", "Por favor, complete todos los campos del formulario")
        return

    if sexo not in ["Masculino", "Femenino", "No binario"]:
        messagebox.showerror("Error", "Por favor ingrese su género")
        return

    try:
        edad = int(edad)
        if edad < 5 or edad > 130:
            messagebox.showerror("Error", "La edad ingresada es inválida")
            return
    except ValueError:
        messagebox.showerror("Error", "La edad debe ser un número válido")
        return
    

    # Generar un ID único para el paciente
    patient_id = str(uuid.uuid4())

    # Directorios temporales
    temp_image_directory = "temp_images/"
    os.makedirs(temp_image_directory, exist_ok=True)

    # Configurar la resolución de conversión de PDF a imagen
    pdf_resolution = 600  # Puedes ajustar esto según tu preferencia

    # Configurar el idioma para el OCR
    language = 'spa'

    # Define las coordenadas de los cuadros (ejemplo)
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
    ]

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
    ]

    try:
        # Convertir el PDF a imágenes
        pages = convert_from_path(pdf_path, dpi=pdf_resolution)

        # Procesar cada página
        texto_final = f"ID: {patient_id}\nNombre: {nombre}\nSexo: {sexo}\nEdad: {edad}\nOficio: {oficio}\nEnfermedad: {enfermedad}\n\n"

        for pageNum, imgBlob in enumerate(pages):
            # Guardar la imagen temporal
            temp_image_path = os.path.join(temp_image_directory, f"temp_page_{pageNum}.jpg")
            imgBlob.save(temp_image_path, "JPEG")

            # Abrir la imagen recién guardada
            img = Image.open(temp_image_path)

            # Recortar la parte superior (1268 píxeles) y la parte inferior (2069 píxeles) de la imagen
            width, height = img.size
            cropped_img = img.crop((0, 1268, width, height - 2069))

            # Recortar las dos categorías adicionales
            # Categoria 1: imagen sector superior
            cat1_img = cropped_img.crop((98, 45, 98 + 4914, 45 + 592))

            # Categoria 2: imagen sector inferior
            cat2_img = cropped_img.crop((89, 2066, 89 + 4932, 2066 + 1188))

            # Procesar cada imagen con OCR y guardar el texto extraído en la variable texto_final
            for cat_img, cuadros in [(cat1_img, cuadros_cat1), (cat2_img, cuadros_cat2)]:
                texto_cuadros = []
                for cuadro in cuadros:
                    x, y, width, height = cuadro
                    cuadro_img = cat_img.crop((x, y, x + width, y + height))

                    # Extrae texto del cuadro con OCR
                    texto = pytesseract.image_to_string(cuadro_img, lang=language).strip()

                    # Verifica si el cuadro está vacío antes de agregarlo
                    if texto:
                        # Buscar la carta más similar al texto extraído
                        carta_texto = get_close_matches(texto, cartas.values(), n=1, cutoff=0.6)
                        if carta_texto:
                            # Obtener el ID de la carta
                            carta_id = list(cartas.keys())[list(cartas.values()).index(carta_texto[0])]

                            # Reemplaza el texto extraído con el ID de la carta
                            texto = f"{carta_id}: {carta_texto[0]}"
                        else:
                            # Si no se encuentra una coincidencia, indica que es desconocido
                            texto = f"Desconocido: {texto}"

                        # Agrega el texto al texto de cuadros
                        texto_cuadros.append(texto)

                # Combina el texto de los cuadros en un solo texto
                texto_final += "\n".join(texto_cuadros) + "\n\n"

    except Exception as e:
        messagebox.showerror("Error", f"Error al procesar {pdf_path}: {e}")

    # Eliminar las imágenes temporales
    for file in os.listdir(temp_image_directory):
        file_path = os.path.join(temp_image_directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    os.rmdir(temp_image_directory)

    # Guardar resultados en un archivo de texto
    guardar_resultados(texto_final, patient_id)
    # Mostrar los resultados en la ventana
    mostrar_resultados(texto_final)
    limpiar_campos()

# Crear la ventana principal
root = tk.Tk()
root.title("Procesamiento de PDFs a Texto")
root.geometry("720x550")
root.configure(bg="#f0f0f0")

# Crear widgets
frame_form = tk.Frame(root, bg="#f0f0f0")
frame_form.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Load the logo
logo = tk.PhotoImage(file="logo-ucen-azul.png.png")  # replace with the path to your logo

# Create a label for the logo and add it to the form
label_logo = tk.Label(frame_form, image=logo, bg="#f0f0f0")
label_logo.image = logo  # keep a reference to avoid garbage collection
label_logo.grid(row=6, columnspan=6)  # change the row and column if needed

label_archivo_pdf = tk.Label(frame_form, text="Archivo PDF:", bg="#f0f0f0", font=("Helvetica", 10))
label_archivo_pdf.grid(row=0, column=0, sticky=tk.W, pady=5)
entry_archivo_pdf = tk.Entry(frame_form, width=50, font=("Helvetica", 10))
entry_archivo_pdf.grid(row=0, column=1, pady=5)
btn_seleccionar_archivo = tk.Button(frame_form, text="Seleccionar Archivo", command=seleccionar_archivo, bg="#f54242", fg="#ffffff", font=("Helvetica", 10))
btn_seleccionar_archivo.grid(row=0, column=2, padx=5, pady=5)

label_nombre = tk.Label(frame_form, text="Nombre:", bg="#f0f0f0", font=("Helvetica", 10))
label_nombre.grid(row=1, column=0, sticky=tk.W, pady=5)
entry_nombre = tk.Entry(frame_form, width=50, font=("Helvetica", 10))
entry_nombre.grid(row=1, column=1, pady=5)

label_sexo = tk.Label(frame_form, text="Género con el que se identifica:", bg="#f0f0f0", font=("Helvetica", 10))
label_sexo.grid(row=2, column=0, sticky=tk.W, pady=5)
combo_sexo = ttk.Combobox(frame_form, values=["Masculino", "Femenino", "No binario"], font=("Helvetica", 10),width=47)
combo_sexo.grid(row=2, column=1, pady=5)
combo_sexo.set('')  # Establecer el valor predeterminado en vacío

label_edad = tk.Label(frame_form, text="Edad:", bg="#f0f0f0", font=("Helvetica", 10))
label_edad.grid(row=3, column=0, sticky=tk.W, pady=5)
entry_edad = tk.Entry(frame_form, width=50, font=("Helvetica", 10))
entry_edad.grid(row=3, column=1, pady=5)

label_oficio = tk.Label(frame_form, text="Oficio:", bg="#f0f0f0", font=("Helvetica", 10))
label_oficio.grid(row=4, column=0, sticky=tk.W, pady=5)
entry_oficio = tk.Entry(frame_form, width=50, font=("Helvetica", 10))
entry_oficio.grid(row=4, column=1, pady=5)

# Crear y posicionar el AutocompleteEntry debajo del campo "Oficio"
label_enfermedad = tk.Label(frame_form, text="Enfermedad:", bg="#f0f0f0", font=("Helvetica", 10))
label_enfermedad.grid(row=5, column=0, sticky=tk.W, pady=5)
autocomplete_entry = AutocompleteEntry(frame_form)
autocomplete_entry.grid(row=5, column=1, pady=5)

# label_enfermedad = tk.Label(frame_form, text="Enfermedad:", bg="#f0f0f0", font=("Helvetica", 10))
# label_enfermedad.grid(row=5, column=0, sticky=tk.W, pady=5)
# entry_enfermedad = tk.Entry(frame_form, width=50, font=("Helvetica", 10))
# entry_enfermedad.grid(row=5, column=1, pady=5)



btn_procesar = tk.Button(frame_form, text="Procesar PDF", command=procesar_pdf, bg="#28a745", fg="#ffffff", font=("Helvetica", 12))
btn_procesar.grid(row=6, columnspan=3, pady=20)

# Iniciar el loop principal de la interfaz
root.mainloop()