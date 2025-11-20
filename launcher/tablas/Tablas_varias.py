
import tkinter as tk
import os
import webbrowser
from PIL import Image, ImageTk

base_dir=os.path.dirname(os.path.abspath(__file__))
pdf_dir=os.path.join(base_dir, "pdfs")
pdf_files=[
    ("Tabla Arte", os.path.join(pdf_dir, "Tabla Arte.pdf")),
    ("Tabla Atacar Objetos", os.path.join(pdf_dir, "Tabla Atacar Objetos.pdf")),
    ("Tabla Condiciones", os.path.join(pdf_dir, "Tabla Condiciones.pdf")),
    ("Tabla Explosivos", os.path.join(pdf_dir, "Tabla Explosivos.pdf")),
    ("Tabla Fab. Obj. Mag.", os.path.join(pdf_dir, "Tabla Fabricar Objetos Mágicos.pdf")),
    ("Tabla Precio Gemas", os.path.join(pdf_dir, "Tabla Precio Gemas.pdf")),
    ("Tabla Recom. Random", os.path.join(pdf_dir, "Tabla Recompensas random.pdf")),
    ("Tabla Servicios", os.path.join(pdf_dir, "Tabla Servicios.pdf")),
    ("Tabla Trans. y precios", os.path.join(pdf_dir, "Tabla Transporte y precios.pdf")),
    ("Tabla Venenos", os.path.join(pdf_dir, "Tabla Venenos.pdf"))
]

def abrir_pdf(ruta):
    if os.path.exists(ruta):
        webbrowser.open_new(ruta)
    else:
        print(f"No se encontró: {ruta}")

ventana=tk.Tk()
ventana.title("Tablas a elegir")
ventana.geometry("750x750")

imagen_fondo=Image.open(os.path.join(base_dir, "background_img", "Tablas_fondo.jpeg"))
imagen_fondo=imagen_fondo.resize((750, 750))
fondo=ImageTk.PhotoImage(imagen_fondo)

label_fondo=tk.Label(ventana, image=fondo)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

frame_central=tk.Frame(ventana)
frame_central.pack(expand=True)

for texto, ruta in pdf_files:
    boton=tk.Button(frame_central, text=texto, width=25, command=lambda r=ruta: abrir_pdf(r))
    boton.pack(pady=5)

boton_cerrar=tk.Button(frame_central, text="Cerrar Tablas", command=ventana.destroy, bg="red", fg="white", width=25)
boton_cerrar.pack(pady=20)

ventana.mainloop()