#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Control de PRep con interfaz negra, edición, límites ±100 y gráfico dinámico (matplotlib)
Guarda datos en 'reputacion.json'
"""

import json, os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")

# ---------------------
# CONFIGURACIÓN BASE
# ---------------------
DATA_FILE = "reputacion.json"

PJS = ["Abel", "Dani", "Daniel", "Josega"]
REGIONES = {
    "co": "Concejo de Vassaris",
    "de": "Delta Noxius",
    "do": "Donum Viliani",
    "im": "Imperio Casthinian",
    "lu": "Luthrandir",
    "re": "Reino de Outlandhi",
}

LIMITE_MIN, LIMITE_MAX = -100, 100


# ---------------------
# FUNCIONES JSON
# ---------------------
def load_data(path=DATA_FILE) -> Dict:
    if not os.path.exists(path):
        return {"next_id": 1, "entries": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        messagebox.showerror("Error al cargar JSON", str(e))
        return {"next_id": 1, "entries": []}


def save_data(data: Dict, path=DATA_FILE):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showerror("Error al guardar JSON", str(e))


# ---------------------
# CÁLCULOS
# ---------------------
def calcular_totales(entries: List[Dict]) -> Dict[str, float]:
    """
    Calcula el total real de cada PJ y el MPG (media de los totales individuales),
    pero muestra los totales limitados entre -100 y 100.
    """
    totals_reales = {pj: 0 for pj in PJS}
    totals_mostrados = {}

    # Sumar puntos reales
    for e in entries:
        pj = e["pj"]
        pts = int(e["puntos"])
        if pj in totals_reales:
            totals_reales[pj] += pts

    # Aplicar límites para mostrar (sin alterar el valor acumulado real)
    for pj, total in totals_reales.items():
        if total > LIMITE_MAX:
            totals_mostrados[pj] = LIMITE_MAX
        elif total < LIMITE_MIN:
            totals_mostrados[pj] = LIMITE_MIN
        else:
            totals_mostrados[pj] = total

    # MPG se calcula usando los valores limitados
    pj_con_puntos = [totals_mostrados[pj] for pj in PJS if totals_reales[pj] != 0]
    mpg = sum(pj_con_puntos) / len(PJS) if pj_con_puntos else 0.0

    # Aplicar límite también al MPG
    if mpg > LIMITE_MAX:
        mpg = LIMITE_MAX
    elif mpg < LIMITE_MIN:
        mpg = LIMITE_MIN

    totals_mostrados["__MPG__"] = mpg
    return totals_mostrados

# ---------------------
# INTERFAZ PRINCIPAL
# ---------------------
class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Control de PRep y MPG")
        self.root.geometry("1000x700")
        self.root.configure(bg="black")

        self.data = load_data()
        self.entries = self.data.get("entries", [])
        self.next_id = self.data.get("next_id", 1)

        self._build_ui()
        self._refresh_all()

    # ------------------------------------
    # Construcción interfaz
    # ------------------------------------
    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TLabel", background="black", foreground="white")
        style.configure("TButton", background="#333", foreground="white")
        style.configure("Treeview", background="#111", fieldbackground="#111", foreground="white")
        style.map("Treeview", background=[("selected", "#444")])

        # ----- Barra superior (resumen) -----
        self.frm_summary = tk.Frame(self.root, bg="black")
        self.frm_summary.pack(fill="x", pady=(10, 5))

        self.lbl_summary = tk.Label(
            self.frm_summary, text="", fg="white", bg="black", font=("Consolas", 12)
        )
        self.lbl_summary.pack()

        # ----- Formulario -----
        frm_top = tk.Frame(self.root, bg="black")
        frm_top.pack(fill="x", pady=10)

        tk.Label(frm_top, text="Personaje:", fg="white", bg="black").grid(row=0, column=0, padx=5)
        self.cmb_pj = ttk.Combobox(frm_top, values=PJS, state="readonly", width=12)
        self.cmb_pj.grid(row=0, column=1, padx=5)
        self.cmb_pj.set(PJS[0])

        tk.Label(frm_top, text="Región:", fg="white", bg="black").grid(row=0, column=2, padx=5)
        self.cmb_region = ttk.Combobox(frm_top, values=list(REGIONES.keys()), state="readonly", width=6)
        self.cmb_region.grid(row=0, column=3, padx=5)
        self.cmb_region.set(list(REGIONES.keys())[0])

        tk.Label(frm_top, text="Puntos:", fg="white", bg="black").grid(row=0, column=4, padx=5)
        self.entry_puntos = ttk.Entry(frm_top, width=10)
        self.entry_puntos.grid(row=0, column=5, padx=5)

        ttk.Button(frm_top, text="Añadir", command=self.add_entry).grid(row=0, column=6, padx=10)
        ttk.Button(frm_top, text="Editar seleccionado", command=self.edit_selected).grid(row=0, column=7, padx=10)
        ttk.Button(frm_top, text="Borrar seleccionado", command=self.delete_selected).grid(row=0, column=8, padx=10)

        # ----- Tabla -----
        cols = ("id", "pj", "region", "puntos", "fecha")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, anchor="center", width=120)
        self.tree.pack(fill="x", padx=10, pady=10)

        # ----- Gráfico matplotlib -----
        self.fig, self.ax = plt.subplots(figsize=(8, 3))
        self.fig.patch.set_facecolor("black")
        self.ax.set_facecolor("black")
        self.ax.tick_params(colors="white", labelsize=9)
        self.ax.spines["bottom"].set_color("white")
        self.ax.spines["left"].set_color("white")
        self.ax.yaxis.label.set_color("green")
        self.ax.xaxis.label.set_color("green")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)

        # ----- Botones inferiores -----
        frm_bottom = tk.Frame(self.root, bg="black")
        frm_bottom.pack(fill="x", pady=10)

        ttk.Button(frm_bottom, text="Guardar JSON", command=self.save_to_file).pack(side="left", padx=10)
        ttk.Button(frm_bottom, text="Cargar JSON", command=self.load_from_file).pack(side="left", padx=10)
        ttk.Button(frm_bottom, text="Reiniciar datos", command=self.reset_data).pack(side="left", padx=10)

        # Doble clic también abre edición
        self.tree.bind("<Double-1>", lambda e: self.edit_selected())

    # ------------------------------------
    # Funciones CRUD
    # ------------------------------------
    def add_entry(self):
        pj = self.cmb_pj.get()
        region = self.cmb_region.get()
        puntos_txt = self.entry_puntos.get().strip()

        if not pj or not region or not puntos_txt:
            messagebox.showwarning("Campos incompletos", "Rellene todos los campos.")
            return
        try:
            puntos = int(puntos_txt)
        except ValueError:
            messagebox.showwarning("Error", "Puntos debe ser un número entero.")
            return

        # Verificar límites antes de añadir
        if not self._check_limits(pj, puntos):
            return

        entry = {
            "id": self.next_id,
            "pj": pj,
            "region": region,
            "puntos": puntos,
            "fecha": datetime.now().isoformat(timespec="seconds"),
        }
        self.entries.append(entry)
        self.next_id += 1
        self.entry_puntos.delete(0, tk.END)
        self._refresh_all()

    def edit_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Editar", "Seleccione una fila.")
            return
        item = self.tree.item(sel[0])
        eid = int(item["values"][0])
        entry = next((e for e in self.entries if e["id"] == eid), None)
        if not entry:
            return

        win = tk.Toplevel(self.root)
        win.title(f"Editar ID {eid}")
        win.configure(bg="black")
        win.resizable(False, False)

        tk.Label(win, text="Personaje:", bg="black", fg="white").grid(row=0, column=0, padx=5, pady=5)
        cmb_pj = ttk.Combobox(win, values=PJS, state="readonly")
        cmb_pj.grid(row=0, column=1, padx=5, pady=5)
        cmb_pj.set(entry["pj"])

        tk.Label(win, text="Región:", bg="black", fg="white").grid(row=1, column=0, padx=5, pady=5)
        cmb_region = ttk.Combobox(win, values=list(REGIONES.keys()), state="readonly")
        cmb_region.grid(row=1, column=1, padx=5, pady=5)
        cmb_region.set(entry["region"])

        tk.Label(win, text="Puntos:", bg="black", fg="white").grid(row=2, column=0, padx=5, pady=5)
        ent_pts = ttk.Entry(win)
        ent_pts.grid(row=2, column=1, padx=5, pady=5)
        ent_pts.insert(0, str(entry["puntos"]))

        def guardar_edicion():
            try:
                new_pts = int(ent_pts.get().strip())
            except ValueError:
                messagebox.showwarning("Error", "Puntos debe ser un número entero.")
                return

            if not self._check_limits(cmb_pj.get(), new_pts, eid):
                return

            entry["pj"] = cmb_pj.get()
            entry["region"] = cmb_region.get()
            entry["puntos"] = new_pts
            entry["fecha"] = datetime.now().isoformat(timespec="seconds")

            self._refresh_all()
            win.destroy()

        ttk.Button(win, text="Guardar cambios", command=guardar_edicion).grid(
            row=3, column=0, columnspan=2, pady=10
        )

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Borrar", "Seleccione una fila.")
            return
        item = self.tree.item(sel[0])
        eid = int(item["values"][0])
        self.entries = [e for e in self.entries if e["id"] != eid]
        self._refresh_all()

    # ------------------------------------
    # Verificación de límites
    # ------------------------------------
    def _check_limits(self, pj, puntos_nuevos, edit_id=None):
        """Evita que un PJ o el MPG excedan ±100."""
        temp_entries = [e for e in self.entries if e["id"] != edit_id]
        temp_entries.append({"id": -1, "pj": pj, "region": "", "puntos": puntos_nuevos, "fecha": ""})
        totals = calcular_totales(temp_entries)

        total_pj = totals[pj]
        mpg = totals["__MPG__"]

        if not (LIMITE_MIN <= total_pj <= LIMITE_MAX):
            messagebox.showwarning(
                "Límite excedido",
                f"El total de {pj} ({total_pj}) excede el rango permitido ({LIMITE_MIN} a {LIMITE_MAX}).",
            )
            return False

        if not (LIMITE_MIN <= mpg <= LIMITE_MAX):
            messagebox.showwarning(
                "Límite MPG excedido",
                f"El MPG resultante ({mpg:.2f}) excede el rango permitido ({LIMITE_MIN} a {LIMITE_MAX}).",
            )
            return False

        return True

    # ------------------------------------
    # Guardar / cargar / reset
    # ------------------------------------
    def save_to_file(self):
        save_data({"next_id": self.next_id, "entries": self.entries})
        messagebox.showinfo("Guardado", f"Datos guardados en {DATA_FILE}")

    def load_from_file(self):
        if messagebox.askyesno("Cargar", "¿Sobrescribir datos actuales?"):
            self.data = load_data()
            self.entries = self.data.get("entries", [])
            self.next_id = self.data.get("next_id", 1)
            self._refresh_all()

    def reset_data(self):
        if messagebox.askyesno("Reiniciar", "¿Vaciar todos los datos?"):
            self.entries = []
            self.next_id = 1
            save_data({"next_id": 1, "entries": []})
            self._refresh_all()

    # ------------------------------------
    # Actualización de UI
    # ------------------------------------
    def _refresh_all(self):
        self._refresh_table()
        self._refresh_summary()
        self._refresh_plot()

    def _refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for e in sorted(self.entries, key=lambda x: x["id"]):
            self.tree.insert("", "end", values=(e["id"], e["pj"], e["region"], e["puntos"], e["fecha"]))

    def _refresh_summary(self):
        totals = calcular_totales(self.entries)
        texto = " | ".join(f"{pj}: {totals[pj]}" for pj in PJS)
        texto += f" || MPG: {totals['__MPG__']:.2f}"
        self.lbl_summary.config(text=texto)

    def _refresh_plot(self):
        totals = calcular_totales(self.entries)
        self.ax.clear()
        self.ax.set_facecolor("black")

        values = [totals[pj] for pj in PJS]
        mpg = totals["__MPG__"]

        bars = self.ax.bar("Abel", values[0], color="#2D5BA0")
        bars = self.ax.bar("Dani", values[1], color="#D0C223")
        bars = self.ax.bar("Daniel", values[2], color="#EE8522")
        bars = self.ax.bar("Guio", values[3], color="#C50606")
        bars = self.ax.bar("Josega", values[4], color="#510F56")
        self.ax.axhline(y=mpg, color="green", linestyle="--", label=f"MPG = {mpg:.2f}")
        self.ax.set_ylabel("Puntos", color="white")
        self.ax.set_xlabel("Personajes", color="white")
        self.ax.legend(facecolor="black", edgecolor="white", labelcolor="white")
        self.ax.tick_params(colors="white")

        for bar in bars:
            height = bar.get_height()
            self.ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 1,
                f"{int(height)}",
                ha="center",
                color="white",
                fontsize=9,
            )

        self.canvas.draw_idle()


# ---------------------
# EJECUCIÓN
# ---------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
