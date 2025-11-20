import tkinter as tk
import subprocess, os
import sys
import threading
from PIL import Image, ImageTk

base_dir=os.path.dirname(os.path.abspath(__file__))
scrypts={
    'Puntos Reputación':os.path.join(base_dir, 'scripts', 'Pts_PRep_y_MPG.py'),
    'Conversor de Viajes': os.path.join(base_dir, 'scripts', 'Conversor para viajes.py'),
    'Generador de Precios': os.path.join(base_dir, 'scripts', 'Generador_precios_rand.py'),
    'Tablas Varias': os.path.join(base_dir, 'scripts', 'Tablas_varias.py')
}

IMAGEN_FONDO=os.path.join(base_dir, 'Icono_launcher.jpeg')
def ejecutar(script):
    try:
        subprocess.Popen(['pythonw', script], creationflags=subprocess.DETACHED_PROCESS)
    except Exception as e:
        tk.messagebox.showerror("Error", f"No se pudo abrir el lanzador:\n{script}\n\n{e}")

def salir():
    ventana.destroy()
    sys.exit(0)

def cargar_fondo_async():
    try:
        imagen=Image.open(IMAGEN_FONDO)
        fondo_img=ImageTk.PhotoImage(imagen)
        ventana.after(0, actualizar_fondo, fondo_img)
    except Exception as e:
        print(f"Error cargando fondo: {e}")

def actualizar_fondo(fondo_img):
    label_fondo.config(image=fondo_img)
    label_fondo.image=fondo_img

ventana=tk.Tk()
ventana.title("Launcher de Rol")
ventana.geometry('650x650')

label_fondo=tk.Label(ventana, bg="#202020")
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

threading.Thread(target=cargar_fondo_async, daemon=True).start()

tk.Label(
    ventana,
    text='Elija herramienta:',
    font=('Arial', 16, 'bold'),
    bg='#202020',
    fg='white'
).pack(pady=25)

for nombre, archivo in scrypts.items():
    tk.Button(
        ventana,
        text=nombre,
        font=('Arial', 12),
        width=25,
        height=1,
        bg='#2e2e2e',
        fg='white',
        relief='raised',
        bd=3,
        command=lambda f=archivo: ejecutar(f)
    ).pack(pady=8)

tk.Button(
    ventana,
    text='Salir',
    font=('Arial', 12, 'bold'),
    width=25,
    bg='#aa3333',
    fg='white',
    relief='raised',
    bd=3,
    command=salir
).pack(pady=50)

ventana.update_idletasks()
ventana.mainloop()