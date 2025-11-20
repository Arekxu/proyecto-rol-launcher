#!/usr/bin/env python

import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys, os

base_dir=(os.path.dirname(os.path.abspath(__file__)))

rarity=["","Común", "Infrecuente", "Raro", "Muy raro", "Legendario"]
oferta=["","Normal", "Descuento", "Incremento"]
usos=["", "Duradero", "Consumible"]
total_compra=0
ultima_compra=0
listado_items=[]

def salir():
    sys.exit(0)

def random_prices(rarity_sel):
    if rarity_sel=="Común":
        return random.randint(75, 125)
    elif rarity_sel=="Infrecuente":
        return random.randint(300, 400)
    elif rarity_sel=="Raro":
        return random.randint(1500, 2500)
    elif rarity_sel=="Muy raro":
        return random.randint(15000, 22000)
    elif rarity_sel=="Legendario":
        return random.randint(70000, 110000)
    
def multiples_usos(usos_sel, rarity_sel):
    base=random_prices(rarity_sel)
    return base if usos_sel=="Duradero" else base/2
    
def tipo_oferta(oferta_sel, usos_sel, rarity_sel):
    base_oferta=multiples_usos(usos_sel, rarity_sel)
    if oferta_sel=="Descuento":
        return round((base_oferta*0.85), -1)
    elif oferta_sel=="Normal":
        return round(base_oferta, -1)
    elif oferta_sel=="Incremento":
        return round((base_oferta*1.1), -1)

def procesar_datos():
    global total_compra, ultima_compra, listado_items
    rarity_sel=rarity_entry.get()
    oferta_sel=oferta_entry.get()
    usos_sel=usos_entry.get()
    nombre_item=nombre_entry.get().strip()

    if not rarity_sel or not oferta_sel or not usos_sel:
        messagebox.showwarning("No se pueden dejar los campos en blanco", "Vuelva a intentarlo.")
        return
    
    if not nombre_item:
        messagebox.showwarning("Nombre vacío", "Introduce el nombre del artículo.")
        return

    compra=int(tipo_oferta(oferta_sel, usos_sel, rarity_sel))
    total_compra+=compra
    ultima_compra=compra

    listado_items.append((nombre_item, compra))
    listado_box.insert(tk.END, f"{nombre_item}: {compra} aurum.")
    
    resultado1=f"Valor del artículo: {compra} aurum.\nTotal acumulado: {int(total_compra)} aurum."
    resultado1_label.config(text=resultado1)

def eliminar_item():
    global total_compra, listado_items

    seleccion=listado_box.curselection()
    if not seleccion:
        messagebox.showwarning("No se ha elegido artículo", "Seleccione uno.")
        return
    
    index=seleccion[0]
    nombre_item, precio_item=listado_items[index]

    total_compra-=precio_item

    listado_items.pop(index)
    listado_box.delete(index)

    resultado1=f"Se eleminó {nombre_item} ({int(precio_item)} aurum).\nTotal acumulado: {int(total_compra)} aurum."
    resultado1_label.config(text=resultado1)

def reiniciar_formulario():
    global total_compra, listado_items, ultima_compra
    rarity_entry.set('')
    oferta_entry.set('')
    usos_entry.set('')
    nombre_entry.delete(0, tk.END)
    listado_box.delete(0, tk.END)
    resultado1_label.config(text="")
    total_compra=0
    ultima_compra=0
    listado_items=[]

ventana=tk.Tk()
ventana.geometry("740x850")

ruta_img=os.path.join(base_dir, "icono.jpeg")
imagen_fondo=Image.open(ruta_img)
imagen_fondo=imagen_fondo.resize((740, 850))
fondo=ImageTk.PhotoImage(imagen_fondo)

label_fondo=tk.Label(ventana, image=fondo)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

# Configuramos la ventana de la interfaz para que tenga una seríe de columnas y filas que más tarde necesitaremos.

ventana.grid_columnconfigure(0, weight=1)
ventana.grid_columnconfigure(1, weight=0)  
ventana.grid_columnconfigure(2, weight=0)  
ventana.grid_columnconfigure(3, weight=1)

ventana.grid_rowconfigure(0, weight=1)
ventana.grid_rowconfigure(7, weight=1)

etiqueta1=tk.Label(ventana, text="Rareza:", bg="white", font=("Arial", 12)).grid(row=1, column=1, padx=10, pady=5, sticky="e")
rarity_entry=ttk.Combobox(ventana, values=rarity, state="readonly")
rarity_entry.current(0)
rarity_entry.grid(row=1, column=2, padx=10, pady=5, sticky="w")

etiqueta2=tk.Label(ventana, text="Uso:", bg="white", font=("Arial", 12)).grid(row=2, column=1, padx=10, pady=5, sticky="e")
usos_entry=ttk.Combobox(ventana, values=usos, state="readonly")
usos_entry.current(0)
usos_entry.grid(row=2, column=2, padx=10, pady=5, sticky="w")

etiqueta3=tk.Label(ventana, text="Oferta:", bg="white", font=("Arial", 12)).grid(row=3, column=1, padx=10, pady=5, sticky="e")
oferta_entry=ttk.Combobox(ventana, values=oferta, state="readonly")
oferta_entry.current(0)
oferta_entry.grid(row=3, column=2, padx=10, pady=5, sticky="w")

etiqueta_nombre=tk.Label(ventana, text="Artículo:", bg="white", font=("Arial",12))
etiqueta_nombre.grid(row=0, column=1, padx=10, pady=5, sticky="e")
nombre_entry=tk.Entry(ventana, width=25)
nombre_entry.grid(row=0, column=2, padx=10, pady=5, sticky="w")

# Creamos el botón que va a realizar el proceso de los datos con la función procesar_datos y la colocamos en la ventana.

botones_frame=tk.Frame(ventana, bg="white")
botones_frame.grid(row=4, column=0, columnspan=4, pady=10)

boton1=tk.Button(botones_frame, text="Calculando precio", command=procesar_datos)
boton1.pack(side="left", padx=10)

eliminar_btn=tk.Button(botones_frame, text="Eliminar artículo", command=eliminar_item)
eliminar_btn.pack(side="left", padx=10)

# Las etiqueta del resultado que vamos a obtener al introducir los datos y darle al botón, junto con sus dimensiones y
# ubicación en la ventana.

resultado1_label = tk.Label(ventana, text="", font=("Arial", 10), bg="white", fg="black")
resultado1_label.grid(row=6, column=0, columnspan=4, pady=(15, 0), sticky="n")

btn_salir=tk.Button(ventana, text='Salir', font=('Arial', 12), width=20, command=salir)
btn_salir.grid(row=7, column=0, columnspan=4, pady=10)

listado_box=tk.Listbox(ventana, width=50, height=8)
listado_box.grid(row=8, column=0, columnspan=4, pady=10)

# Por último tenemos el botón de reinicio de los apartados de datos, y para ello utilizaremos la función reiniciar_formulario.
reiniciar_btn = tk.Button(ventana, text="¿Eso es todo?", command=reiniciar_formulario)
reiniciar_btn.grid(row=5, column=1, columnspan=2, pady=5)



# Este apartado evita que la ventana se cierre inmediatamente cuando se abra y permanezca hasta que decidamos cerrarla.

ventana.mainloop()