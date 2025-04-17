import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# -------------------- BASE DE DATOS --------------------
def conectar_db():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE,
            precio REAL,
            cantidad INTEGER
        )
    """)
    conn.commit()
    return conn

conn = conectar_db()

def agregar_producto():
    nombre = nombre_entry.get().strip()
    precio = precio_entry.get()
    cantidad = cantidad_entry.get()

    if not nombre or not precio or not cantidad:
        messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
        return

    try:
        precio = float(precio)
        cantidad = int(cantidad)
    except ValueError:
        messagebox.showerror("Error", "Precio debe ser número y cantidad un entero.")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre = ?", (nombre,))
    existente = cursor.fetchone()

    if existente:
        cursor.execute("UPDATE productos SET cantidad = cantidad + ?, precio = ? WHERE nombre = ?", (cantidad, precio, nombre))
    else:
        cursor.execute("INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)", (nombre, precio, cantidad))

    conn.commit()
    actualizar_tabla()
    limpiar_entradas()

def eliminar_producto():
    seleccionado = tabla.focus()
    if not seleccionado:
        messagebox.showwarning("Selecciona un producto", "Selecciona un producto para eliminar.")
        return

    nombre = tabla.item(seleccionado)["values"][0]
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE nombre = ?", (nombre,))
    conn.commit()
    actualizar_tabla()

def aumentar_stock():
    actualizar_stock(+1)

def disminuir_stock():
    actualizar_stock(-1)

def actualizar_stock(cambio):
    seleccionado = tabla.focus()
    if not seleccionado:
        messagebox.showwarning("Selecciona un producto", "Selecciona un producto.")
        return

    nombre = tabla.item(seleccionado)["values"][0]
    cursor = conn.cursor()
    cursor.execute("SELECT cantidad FROM productos WHERE nombre = ?", (nombre,))
    resultado = cursor.fetchone()
    if resultado:
        nueva_cantidad = resultado[0] + cambio
        if nueva_cantidad < 0:
            messagebox.showerror("Error", "No puedes tener cantidad negativa.")
            return
        cursor.execute("UPDATE productos SET cantidad = ? WHERE nombre = ?", (nueva_cantidad, nombre))
        conn.commit()
        actualizar_tabla()

def buscar_producto():
    nombre = buscar_entry.get().strip()
    if not nombre:
        actualizar_tabla()
        return

    for item in tabla.get_children():
        tabla.delete(item)

    cursor = conn.cursor()
    cursor.execute("SELECT nombre, precio, cantidad FROM productos WHERE nombre LIKE ?", (f"%{nombre}%",))
    for nombre, precio, cantidad in cursor.fetchall():
        tabla.insert("", "end", values=(nombre, precio, cantidad))

def actualizar_tabla():
    for item in tabla.get_children():
        tabla.delete(item)

    cursor = conn.cursor()
    cursor.execute("SELECT nombre, precio, cantidad FROM productos")
    for nombre, precio, cantidad in cursor.fetchall():
        tabla.insert("", "end", values=(nombre, precio, cantidad))

def limpiar_entradas():
    nombre_entry.delete(0, tk.END)
    precio_entry.delete(0, tk.END)
    cantidad_entry.delete(0, tk.END)

def editar_cantidad():
    seleccionado = tabla.focus()
    if not seleccionado:
        messagebox.showwarning("Selecciona un producto", "Selecciona un producto de la lista.")
        return

    try:
        nueva_cantidad = int(nueva_cantidad_entry.get())
        if nueva_cantidad < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Ingresa una cantidad válida (entero positivo).")
        return

    nombre = tabla.item(seleccionado)["values"][0]
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET cantidad = ? WHERE nombre = ?", (nueva_cantidad, nombre))
    conn.commit()
    actualizar_tabla()
    nueva_cantidad_entry.delete(0, tk.END)


# -------------------- INTERFAZ --------------------
ventana = tk.Tk()
ventana.title("Inventario para Tienda")

# Entradas
tk.Label(ventana, text="Nombre:").grid(row=0, column=0)
tk.Label(ventana, text="Precio:").grid(row=1, column=0)
tk.Label(ventana, text="Cantidad:").grid(row=2, column=0)

nombre_entry = tk.Entry(ventana)
precio_entry = tk.Entry(ventana)
cantidad_entry = tk.Entry(ventana)

nombre_entry.grid(row=0, column=1)
precio_entry.grid(row=1, column=1)
cantidad_entry.grid(row=2, column=1)

tk.Button(ventana, text="Agregar / Actualizar", command=agregar_producto).grid(row=3, column=0, columnspan=2)
tk.Button(ventana, text="Eliminar Producto", command=eliminar_producto).grid(row=4, column=0, columnspan=2)

# Tabla de inventario
tabla = ttk.Treeview(ventana, columns=("Nombre", "Precio", "Cantidad"), show="headings")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Precio", text="Precio")
tabla.heading("Cantidad", text="Cantidad")
tabla.grid(row=5, column=0, columnspan=2, pady=10)

# Controles de cantidad
tk.Button(ventana, text="Aumentar Cantidad", command=aumentar_stock).grid(row=6, column=0)
tk.Button(ventana, text="Disminuir Cantidad", command=disminuir_stock).grid(row=6, column=1)
tk.Label(ventana, text="Nueva cantidad:").grid(row=9, column=0)
nueva_cantidad_entry = tk.Entry(ventana)
nueva_cantidad_entry.grid(row=9, column=1)

tk.Button(ventana, text="Actualizar cantidad", command=editar_cantidad).grid(row=10, column=0, columnspan=2)


# Búsqueda
tk.Label(ventana, text="Buscar producto:").grid(row=7, column=0)
buscar_entry = tk.Entry(ventana)
buscar_entry.grid(row=7, column=1)
tk.Button(ventana, text="Buscar", command=buscar_producto).grid(row=8, column=0, columnspan=2, pady=5)

actualizar_tabla()
ventana.mainloop()
conn.close()
