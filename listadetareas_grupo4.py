import tkinter as tk
from tkinter import messagebox
import mysql.connector

conexión = mysql.connector.connect(user='root', password='020306', host='localhost', database='bdpython', port="3306")

def agregar_tarea_a_bd(tarea, estado):
    try:
        cursor = conexión.cursor()
        if estado == "Por hacer":
            query = "INSERT INTO tareas_por_hacer (tarea) VALUES (%s)"
        elif estado == "En proceso":
            query = "INSERT INTO tareas_en_proceso (tarea) VALUES (%s)"
        elif estado == "Terminado":
            query = "INSERT INTO tareas_terminado (tarea) VALUES (%s)"
        
        cursor.execute(query, (tarea,))
        conexión.commit()
        cursor.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Error en la base de datos", f"No se pudo agregar la tarea a la tabla {estado}: {e}")

def agregar_tarea():
    tarea = ingreso_tarea.get()
    if tarea:
        lista_por_hacer.insert(tk.END, tarea)  
        agregar_tarea_a_bd(tarea, "Por hacer")  
        ingreso_tarea.delete(0, tk.END)
    else:
        messagebox.showwarning("Entrada vacía", "Por favor, ingrese una tarea.")

def eliminar_tarea():
    for lista in [lista_por_hacer, lista_en_proceso, lista_terminado]:
        seleccion = lista.curselection()
        if seleccion:
            lista.delete(seleccion)
            return
    messagebox.showwarning("Selección vacía", "Por favor, seleccione una tarea a eliminar.")

def cambiar_estado(nuevo_estado):
    for lista in [lista_por_hacer, lista_en_proceso, lista_terminado]:
        seleccion = lista.curselection()
        if seleccion:
            tarea = lista.get(seleccion)
            lista.delete(seleccion)  
            agregar_tarea_a_bd(tarea, nuevo_estado)  
            
            if nuevo_estado == "Por hacer":
                lista_por_hacer.insert(tk.END, tarea)
            elif nuevo_estado == "En proceso":
                lista_en_proceso.insert(tk.END, tarea)
            elif nuevo_estado == "Terminado":
                lista_terminado.insert(tk.END, tarea)
            return
    messagebox.showwarning("Selección vacía", "Por favor, seleccione una tarea para cambiar su estado.")

ventana = tk.Tk()
ventana.title('Lista de tareas')
ventana.geometry('600x600')
ventana.configure(bg='white')

frame = tk.Frame(ventana, bg='white')
frame.pack(pady=10, fill='both', expand=True)

ingreso_tarea = tk.Entry(frame, bg='white', fg='black')
ingreso_tarea.pack(pady=5, fill='x')

boton_agregar = tk.Button(frame, text='Agregar tarea', command=agregar_tarea, bg='red', fg='white', width=15)
boton_agregar.pack(pady=5, fill='x')

frame_listas = tk.Frame(frame, bg='white')
frame_listas.pack(pady=10, anchor='center')

label_por_hacer = tk.Label(frame_listas, text='Por hacer', bg='white', fg='red')
label_por_hacer.grid(row=0, column=0, padx=20, pady=5)
label_en_proceso = tk.Label(frame_listas, text='En proceso', bg='white', fg='red')
label_en_proceso.grid(row=0, column=1, padx=20, pady=5)
label_terminado = tk.Label(frame_listas, text='Terminado', bg='white', fg='red')
label_terminado.grid(row=0, column=2, padx=20, pady=5)

lista_por_hacer = tk.Listbox(frame_listas, bg='white', fg='black', height=15, width=20)
lista_por_hacer.grid(row=1, column=0, padx=20, pady=5)
lista_en_proceso = tk.Listbox(frame_listas, bg='white', fg='black', height=15, width=20)
lista_en_proceso.grid(row=1, column=1, padx=20, pady=5)
lista_terminado = tk.Listbox(frame_listas, bg='white', fg='black', height=15, width=20)
lista_terminado.grid(row=1, column=2, padx=20, pady=5)

boton_eliminar = tk.Button(frame, text='Eliminar tarea', command=eliminar_tarea, bg='red', fg='white', width=15)
boton_eliminar.pack(pady=5, fill='x')

boton_por_hacer = tk.Button(frame, text='Mover a Por hacer', command=lambda: cambiar_estado("Por hacer"), bg='red', fg='white', width=15)
boton_por_hacer.pack(pady=2, fill='x')
boton_en_proceso = tk.Button(frame, text='Mover a En proceso', command=lambda: cambiar_estado("En proceso"), bg='red', fg='white', width=15)
boton_en_proceso.pack(pady=2, fill='x')
boton_terminado = tk.Button(frame, text='Mover a Terminado', command=lambda: cambiar_estado("Terminado"), bg='red', fg='white', width=15)
boton_terminado.pack(pady=2, fill='x')

ventana.mainloop()
