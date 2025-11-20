#!/usr/bin/env python

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys, os

base_dir=os.path.dirname(os.path.abspath(__file__))
vehiculos=["","Aeronave", "Galeon", "Velero", "Carabela", "Bote", "Carruaje", "Caminando"]
velocidades=["","Rápida", "Normal", "Lenta"]
path_img=os.path.join(base_dir, "viaje.jpeg")

class DatosUsuario:
    def __init__(self):
        self.pies = 0
        self.vehiculo = ""
        self.velocidad = ""

datos = DatosUsuario()

def salir():
    ventana.destroy()
    sys.exit(0)

def procesar_datos():
    datos.vehiculo=vehiculo_combobox.get()
    datos.velocidad=velocidad_combobox.get()
    pies=pies_entry.get()

    if not datos.vehiculo or not pies:
        messagebox.showwarning("Hay campos en blanco", "Vuelva a intentarlo.")
        return
    elif datos.vehiculo=="Caminando":
        if not datos.velocidad:
            messagebox.showwarning("Error", "Falta elegir la velocidad")
            return
              
    try:
        datos.pies=int(pies)
    except ValueError:
        messagebox.showwarning("Error", "Ni para escribir números vales...")

    resultado1=f"Utilizando {datos.vehiculo} tardarían {tiempo_viajando()}."
    
    resultado1_label.config(text=resultado1)
    

def pies_a_millas():
    conversion=(datos.pies*60)/8
    return round(conversion)

def velocidad_vehiculo():
    if datos.vehiculo=="Aeronave":
        if datos.velocidad=="Rápida":
            return 8
        elif datos.velocidad=="Normal":
            return 8
        elif datos.velocidad=="Lenta":
            return 8
        return 8
    elif datos.vehiculo=="Galeon":
        if datos.velocidad=="Rápida":
            return 4
        elif datos.velocidad=="Normal":
            return 4
        elif datos.velocidad=="Lenta":
            return 4
        return 4
    elif datos.vehiculo=="Velero":
        if datos.velocidad=="Rápida":
            return 1
        elif datos.velocidad=="Normal":
            return 1
        elif datos.velocidad=="Lenta":
            return 1
        return 1
    elif datos.vehiculo=="Carabela":
        if datos.velocidad=="Rápida":
            return 3
        elif datos.velocidad=="Normal":
            return 3
        elif datos.velocidad=="Lenta":
            return 3
        return 3
    elif datos.vehiculo=="Bote":
        if datos.velocidad=="Rápida":
            return 1.5
        elif datos.velocidad=="Normal":
            return 1.5
        elif datos.velocidad=="Lenta":
            return 1.5
        return 1.5
    elif datos.vehiculo=="Carruaje":
        if datos.velocidad=="Rápida":
            return 4
        elif datos.velocidad=="Normal":
            return 4
        elif datos.velocidad=="Lenta":
            return 4
        return 4
    elif datos.vehiculo=="Caminando":
        if datos.velocidad=="Rápida":
            return 4
        elif datos.velocidad=="Normal":
            return 3
        elif datos.velocidad=="Lenta":
            return 2
    return

def tiempo_viajando():
    total_horas=pies_a_millas()/velocidad_vehiculo()
    dias=total_horas//24
    horas_restantes=total_horas%24
    dias_y_horas=f"{int(dias)} día/s y {round(horas_restantes)} hora/s."
    return dias_y_horas


def reiniciar_formulario():
    vehiculo_combobox.set('')
    velocidad_combobox.set('')
    pies_entry.delete(0, tk.END)
    resultado1_label.config(text="")
    reiniciar_btn.pack_forget()

ventana=tk.Tk()
ventana.geometry("740x850")

imagen_fondo=Image.open(path_img).resize((740, 850))
fondo=ImageTk.PhotoImage(imagen_fondo)
label_fondo=tk.Label(ventana, image=fondo)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

# Configuramos la ventana de la interfaz para que tenga una seríe de columnas y filas que más tarde necesitaremos.

ventana.grid_columnconfigure((0, 3), weight=1)
ventana.grid_rowconfigure((0, 7), weight=1)


etiqueta1=tk.Label(ventana, text="Vehículo:", bg="white", font=("Arial", 12)).grid(row=1, column=1, padx=10, pady=5, sticky="e")
vehiculo_combobox=ttk.Combobox(ventana, values=vehiculos, state="readonly")
vehiculo_combobox.current(0)
vehiculo_combobox.grid(row=1, column=2, padx=10, pady=5, sticky="w")

etiqueta2=tk.Label(ventana, text="Velocidad:", bg="white", font=("Arial", 12)).grid(row=2, column=1, padx=10, pady=5, sticky="e")
velocidad_combobox=ttk.Combobox(ventana, values=velocidades, state="readonly")
velocidad_combobox.current(0)
velocidad_combobox.grid(row=2, column=2, padx=10, pady=5, sticky="w")

etiqueta3=tk.Label(ventana, text="Pies:", bg="white", font=("Arial", 12)).grid(row=3, column=1, padx=10, pady=5, sticky="e")
pies_entry= tk.Entry(ventana)
pies_entry.grid(row=3, column=2, padx=10, pady=5, sticky="w")

# Creamos el botón que va a realizar el proceso de los datos con la función procesar_datos y la colocamos en la ventana.

boton1=tk.Button(ventana, text="Calculando tiempo", command=procesar_datos)
boton1.grid(row=4, column=1, columnspan=2, pady=10)

# Las etiqueta del resultado que vamos a obtener al introducir los datos y darle al botón, junto con sus dimensiones y
# ubicación en la ventana.

resultado1_label = tk.Label(ventana, text="", font=("Arial", 10), bg="white", fg="blue")
resultado1_label.grid(row=6, column=0, columnspan=4, pady=(15, 0), sticky="n")

btn_salir=tk.Button(ventana, text='Salir', font=('Arial', 12), width=20, command=salir)
btn_salir.grid(row=7, column=0, columnspan=4, pady=10)

# Por último tenemos el botón de reinicio de los apartados de datos, y para ello utilizaremos la función reiniciar_formulario.

reiniciar_btn = tk.Button(ventana, text="¿Otro trayecto?", command=reiniciar_formulario)
reiniciar_btn.grid(row=5, column=1, columnspan=2, pady=5)

# Este apartado evita que la ventana se cierre inmediatamente cuando se abra y permanezca hasta que decidamos cerrarla.

ventana.mainloop()