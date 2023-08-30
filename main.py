################################################################
#  Script      : main.py
#  Version     : 1.0
#  Descripción : Script que almacena datos en un repositorio de
#                SQLite3 con interfaz grafica TKinter     
#  Autor       : Raúl Ibañez M.
#  Fecha       : 29-08-2023
###############################################################
from tkinter import ttk, messagebox
from tkinter import *

import sqlite3

class App:
	# dirextorio del repositorio de Datos 
    db_name = 'data.db'

    def __init__(self, window):
		# Inicialización de la Ventana Principal 
        self.wind = window
        self.wind.title('Gestor de Contraseñas')
        # Despliegue de la Tabla de Datos
        #self.tree = ttk.Treeview(height = 10, columns = 4)
        self.tree = ttk.Treeview(columns = ("SITIO","CORREO", "EXPIRA","USUARIO","CONTRASEÑA", "COMENTARIO"))
        self.tree.grid(row = 4, column = 0, columnspan = 4)
        self.tree.heading('#0', text = 'ID', anchor = CENTER)
        self.tree.heading('SITIO', text = 'SITIO', anchor = CENTER)
        self.tree.heading('CORREO', text = 'CORREO', anchor = CENTER)
        self.tree.heading('EXPIRA', text = 'EXPIRA', anchor = CENTER)
        self.tree.heading('USUARIO', text = 'USUARIO', anchor = CENTER)
        self.tree.heading('CONTRASEÑA', text = 'CONTRASEÑA', anchor = CENTER)
        self.tree.heading('COMENTARIO', text = 'COMENTARIO', anchor = CENTER)

        # Botones de la Tabla Principal
        ttk.Button(text = 'AGREGAR', command = self.new_record).grid(row = 5, column = 0, sticky = W + E) 
        ttk.Button(text = 'EDITAR', command = self.edit_record).grid(row = 5, column = 1, sticky = W + E)
        ttk.Button(text = 'BORRAR', command = self.delete_record).grid(row = 5, column = 2, sticky = W + E)
        ttk.Button(text = 'SALIR', command=window.destroy).grid(row = 5, column = 3, sticky = W + E)

        # rellena la Tabla
        self.get_records()


    # Funcion que Ejecuta Querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result


    # Obtiene datos del repositorio de datos
    def get_records(self):
        # Limpia la Tabla 
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # Obtiene la data
        query = 'SELECT * FROM gestor ORDER BY server DESC'
        db_rows = self.run_query(query)
        # rellena con data
        for row in db_rows:
            self.tree.insert('', 0, text = row[0], values = (row[1], row[2], row[3], row[4], row[5], row[6]))

    # Agrega registros al Repositorio de datos         
    def new_record(self):
        self.add_wind = Toplevel()
        self.add_wind.geometry('280x200')
        self.add_wind.resizable(width=0, height=0)
        #-------------------------------------
        # Etiquetas de Campos
        l0 = Label(self.add_wind, text = "NUEVO REGISTRO")
        l1 = Label(self.add_wind, text = "SITIO:")
        l2 = Label(self.add_wind, text = "CORREO:")
        l3 = Label(self.add_wind, text = "EXPIRA:")
        l4 = Label(self.add_wind, text = "USUARIO:")
        l5 = Label(self.add_wind, text = "CONTRASEÑA:")
        l6 = Label(self.add_wind, text = "COMENTARIOS:")

        l0.grid(row = 0, columnspan=2, sticky = W, pady = 2)
        l1.grid(row = 1, column = 0, sticky = W, pady = 2)
        l2.grid(row = 2, column = 0, sticky = W, pady = 2)
        l3.grid(row = 3, column = 0, sticky = W, pady = 2)
        l4.grid(row = 4, column = 0, sticky = W, pady = 2)
        l5.grid(row = 5, column = 0, sticky = W, pady = 2)
        l6.grid(row = 6, column = 0, sticky = W, pady = 2)
        #-------------------------------------
        # Campos
        e1 = Entry(self.add_wind)
        e2 = Entry(self.add_wind)
        e3 = Entry(self.add_wind)
        e4 = Entry(self.add_wind)
        e5 = Entry(self.add_wind)
        e6 = Entry(self.add_wind)

        e1.grid(row = 1, column = 1, pady = 2)
        e2.grid(row = 2, column = 1, pady = 2)
        e3.grid(row = 3, column = 1, pady = 2)
        e4.grid(row = 4, column = 1, pady = 2)
        e5.grid(row = 5, column = 1, pady = 2)
        e6.grid(row = 6, column = 1, pady = 2)

        #-------------------------------------
        # Botones
        self.accion = "Agregar" 
        codigo = 0
        Button(self.add_wind, text = 'GUARDAR', command = lambda: self.save_record(self.accion, e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get(), codigo)).grid(row = 7, column = 2, sticky = W)

    # Edita / Actualiza registros Existentes del Repositorio de datos         
    def edit_record(self):
        try:
            # Obtener el ID del primer elemento seleccionado.
            item = self.tree.selection()[0]
        except IndexError:
            # Si la tupla está vacía, entonces no hay ningún
            # elemento seleccionado.
            messagebox.showwarning(
                message="Debe seleccionar un elemento.",
                title="No hay selección")
        else:
            # A partir de este ID retornar el texto del elemento.
            # text = self.tree.item(item, option="text")
            # Mostrarlo en un cuadro de diálogo.
            # messagebox.showinfo(message=text, title="Selección")
            codigo = self.tree.item(item, option="text")            
            sitio = self.tree.item(self.tree.selection())['values'][0]
            correo = self.tree.item(self.tree.selection())['values'][1]
            fecha = self.tree.item(self.tree.selection())['values'][2]
            usuario = self.tree.item(self.tree.selection())['values'][3]
            contraseña = self.tree.item(self.tree.selection())['values'][4]
            comentario = self.tree.item(self.tree.selection())['values'][5]
            #-------------------------------------
            self.edit_wind = Toplevel()
            self.edit_wind.geometry('280x200')
            self.edit_wind.resizable(width=0, height=0)
            #-------------------------------------
            # Etiquetas de Campos
            l0 = Label(self.edit_wind, text = "ACTUALIZAR REGISTRO " + str(codigo))
            l1 = Label(self.edit_wind, text = "SITIO:")
            l2 = Label(self.edit_wind, text = "CORREO:")
            l3 = Label(self.edit_wind, text = "EXPIRA:")
            l4 = Label(self.edit_wind, text = "USUARIO:")
            l5 = Label(self.edit_wind, text = "CONTRASEÑA:")
            l6 = Label(self.edit_wind, text = "COMENTARIOS:")

            l0.grid(row = 0, columnspan=2, sticky = W, pady = 2)
            l1.grid(row = 1, column = 0, sticky = W, pady = 2)
            l2.grid(row = 2, column = 0, sticky = W, pady = 2)
            l3.grid(row = 3, column = 0, sticky = W, pady = 2)
            l4.grid(row = 4, column = 0, sticky = W, pady = 2)
            l5.grid(row = 5, column = 0, sticky = W, pady = 2)
            l6.grid(row = 6, column = 0, sticky = W, pady = 2)
            #-------------------------------------
            # Campos
            e1 = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = sitio))
            e2 = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = correo))
            e3 = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = fecha))
            e4 = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = usuario))
            e5 = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = contraseña))
            e6 = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = comentario))

            e1.grid(row = 1, column = 1, pady = 2)
            e2.grid(row = 2, column = 1, pady = 2)
            e3.grid(row = 3, column = 1, pady = 2)
            e4.grid(row = 4, column = 1, pady = 2)
            e5.grid(row = 5, column = 1, pady = 2)
            e6.grid(row = 6, column = 1, pady = 2)

            #-------------------------------------
            # Botones
            self.accion = "Editar" 
            Button(self.edit_wind, text = 'GUARDAR', command = lambda: self.save_record(self.accion, e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get(), codigo)).grid(row = 7, column = 2, sticky = W)

    # Elimina Registros del Repositorio
    def delete_record(self):
        try:
            # Obtener el ID del primer elemento seleccionado.
            item = self.tree.selection()[0]
        except IndexError:
            # Si la tupla está vacía, entonces no hay ningún
            # elemento seleccionado.
            messagebox.showwarning(
                message="Debe seleccionar un elemento.",
                title="No hay selección")
        else:            
            # A partir de este ID retornar el texto del elemento.
            # text = self.tree.item(item, option="text")
            # Mostrarlo en un cuadro de diálogo.
            # messagebox.showinfo(message=text, title="Selección")
            codigo = self.tree.item(item, option="text")
            query = 'DELETE FROM gestor WHERE id_sitio = ?'
            self.run_query(query, (codigo, ))
            print("Registro ["+ str(codigo) +"] Eliminado!")
            self.get_records()


    # Guarda los datos en el repositorio    
    def save_record(self, accion, e1, e2, e3, e4, e5, e6, codigo):
        if accion== "Agregar":
            if len(e1) != 0 and len(e2) != 0 and len(e3) !=0 and len(e4) !=0 and len(e5) !=0 and len(e6) !=0:
                query = 'INSERT INTO gestor VALUES(NULL, ?, ?, ?, ?, ?, ?)'
                parameters =  (e1, e2, e3, e4, e5, e6)
                self.run_query(query, parameters)
                print("Se agregó un registro!")
            else:
                print("Error! Campos en blanco")
            self.add_wind.destroy()
        if accion=="Editar":
            if len(e1) != 0 and len(e2) != 0 and len(e3) !=0 and len(e4) !=0 and len(e5) !=0 and len(e6) !=0:
                query = 'UPDATE gestor SET server=?, email=?, expira=?, usuario=?, contra=?, observ=? WHERE id_sitio=?'
                parameters =  (e1, e2, e3, e4, e5, e6, codigo)
                self.run_query(query, parameters)
                print("Registro ["+ str(codigo) +"] Actualizado!")
            else:
                print("Error! Campos en blanco")
            self.edit_wind.destroy()
        self.get_records()


if __name__ == '__main__':
    window = Tk()
    application = App(window)
    window.mainloop()