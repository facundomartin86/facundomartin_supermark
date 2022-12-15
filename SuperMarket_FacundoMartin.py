
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from datetime import datetime


def execute_query(sql, params=()):
    conn = sqlite3.connect('db_Supermarket_FacundoMartin.db')
    cursor = conn.cursor()
    result = None
    try:
        cursor.execute(sql, params)
        conn.commit()
        result = cursor.fetchall()
    except Exception as e:
        print(e)
    conn.close()
    return result

def create_productos_table():
    sql = '''CREATE TABLE IF NOT EXISTS productos(
             producto_id INTEGER PRIMARY KEY,
             nombre VARCHAR(70) NOT NULL,
             precio VARCHAR(50) NOT NULL,
             stock VARCHAR(50) NOT NULL
             )'''
    execute_query(sql)

def create_ventas_table():
    sql = '''CREATE TABLE IF NOT EXISTS ventas(
             venta_id INTEGER PRIMARY KEY AUTOINCREMENT,
             producto VARCHAR(50) NOT NULL,
             precio VARCHAR(70) NOT NULL,
             cantidad VARCHAR(50) NOT NULL,
             subtotal VARCHAR(50) NOT NULL,
             cerrada INTEGER DEFAULT 0 NOT NULL
             )'''
    execute_query(sql)

def create_reportes_table():
    sql = '''CREATE TABLE IF NOT EXISTS reportes(
             reporte_id INTEGER PRIMARY KEY AUTOINCREMENT,
             detalle VARCHAR(100) NOT NULL,
             fecha VARCHAR(50) NOT NULL,
             hora VARCHAR(50) NOT NULL,
             total VARCHAR(50) NOT NULL
             )'''
    execute_query(sql)

create_productos_table()
create_ventas_table()
create_reportes_table()

def detalle_producto(id_producto):
  sql='SELECT * FROM productos WHERE producto_id = ?'
  params = (id_producto)
  p= execute_query(sql, params)
  return p

class Productos:
    def __init__(self, master):
        self.master = master
        self.master.title("Productos")
        self.master.geometry("1100x600")
        self.master.configure(background="light grey")
        self.frame = Frame(self.master)
        self.frame.pack()

        self.texto = Label(self.frame, text="PRODUCTOS")
        self.texto.config(font=("Arial", 26))
        self.texto.grid(row=0, column=0, columnspan=2)

        self.texto = Label(self.frame, text="ID")
        self.texto.config(font=("Arial"))
        self.texto.grid(row=1, column=0, sticky="e")

        self.producto_id = Entry(self.frame)
        self.producto_id.grid(row=1, column=1, sticky="w")

        self.texto = Label(self.frame, text="NOMBRE")
        self.texto.config(font=("Arial"))
        self.texto.grid(row=2, column=0, sticky="e")

        self.nombre = Entry(self.frame)
        self.nombre.grid(row=2, column=1, sticky="w")

        self.texto = Label(self.frame, text="PRECIO")
        self.texto.config(font=("Arial"))
        self.texto.grid(row=3, column=0, sticky="e")

        self.precio = Entry(self.frame)
        self.precio.grid(row=3, column=1, sticky="w")

        self.texto = Label(self.frame, text="STOCK")
        self.texto.config(font=("Arial"))
        self.texto.grid(row=4, column=0, sticky="e")

        self.stock = Entry(self.frame)
        self.stock.grid(row=4, column=1, padx=5, sticky="w")

        self.agre = Button(self.frame, text="Agregar", command=self.agregar)
        self.agre.grid(row=6, column=0, padx=5, sticky="e",pady=5)

        self.limpia = Button(self.frame, text="Limpiar", command=self.limpiar)
        self.limpia.grid(row=6, column=1, padx=5, sticky="w",pady=5)
      
        self.tree = ttk.Treeview(self.frame,height = 15,columns=("id", "nombre", "precio", "stock"))
        self.tree.heading("#0", text="")
        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="Nombre")
        self.tree.heading("#3", text="Precio")
        self.tree.heading("#4", text="Stock")
        self.tree.grid(row=7, column=0, columnspan=2, padx=5, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.selected_item)
        
        verscrlbar = ttk.Scrollbar(self.frame,orient ="vertical",command = self.tree.yview)
        verscrlbar.grid(column=2, row=7, sticky='w')
        self.tree.configure(xscrollcommand = verscrlbar.set)
        
        self.eliminar = Button(self.frame, text="Eliminar", command=self.eliminar)
        self.eliminar.grid(row=16, column=0, padx=5, sticky="e")

        self.actualizar = Button(self.frame, text="Actualizar", command=self.actualizar)
        self.actualizar.grid(row=16, column=1, padx=5, sticky="w")
        
        self.show()

    def show(self):
        self.tree.delete(*self.tree.get_children())
        sql = "SELECT * FROM productos"
        rows = execute_query(sql)
        for row in rows:
            self.tree.insert("", END, text=row[1], values=(row[0], row[1], row[2], row[3]))

    def agregar(self):
        if self.producto_id.get() == '' or self.nombre.get() == '' or self.precio.get() == '' or self.stock.get() == '':
            messagebox.showerror("Error", "Todos los campos son requeridos.")
        else:
            sql = "INSERT INTO productos(producto_id, nombre, precio, stock) VALUES(?, ?, ?, ?)"
            params = (self.producto_id.get(), self.nombre.get(), self.precio.get(), self.stock.get())
            execute_query(sql, params)
            self.show()
            self.limpiar()
            messagebox.showinfo("Bien", "Producto agregado correctamente.")

    def eliminar(self):
        if self.producto_id.get() == '':
            messagebox.showerror("Error", "Seleccione un registro.")
        else:
            result = messagebox.askquestion("Borrar", "¿Desea eliminar este registro?", icon="warning")
            if result == 'yes':
                sql = "DELETE FROM productos WHERE producto_id = ?"
                params = (self.producto_id.get(),)
                execute_query(sql, params)
                self.show()
                self.limpiar()
                messagebox.showinfo("Bien", "Producto eliminado correctamente.")

    def actualizar(self):
        if self.producto_id.get() == '' or self.nombre.get() == '' or self.precio.get() == '' or self.stock.get() == '':
            messagebox.showerror("Error", "Seleccione un registro.")
        else:
            sql = "UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE producto_id = ?"
            params = (self.nombre.get(), self.precio.get(), self.stock.get(), self.producto_id.get())
            execute_query(sql, params)
            self.show()
            self.limpiar()
            messagebox.showinfo("Bien", "Producto actualizado correctamente.")

    def selected_item(self, event):
        curItem = self.tree.focus()
        contents = (self.tree.item(curItem))
        selected_item = contents['values']
        self.producto_id.delete(0, END)
        self.producto_id.insert(0, selected_item[0])
        self.nombre.delete(0, END)
        self.nombre.insert(0, selected_item[1])
        self.precio.delete(0, END)
        self.precio.insert(0, selected_item[2])
        self.stock.delete(0, END)
        self.stock.insert(0, selected_item[3])

    def limpiar(self):
        self.producto_id.delete(0, END)
        self.nombre.delete(0, END)
        self.precio.delete(0, END)
        self.stock.delete(0, END)


class Ventas:
    def __init__(self, master):
        self.master = master
        self.master.title("Ventas")
        self.master.geometry("1300x650")
        self.master.configure(background="light grey")
        self.frame = Frame(self.master)
        self.frame.pack()

        self.texto = Label(self.frame, text="VENTAS")
        self.texto.config(font=("Arial", 26))
        self.texto.grid(row=0, column=0, columnspan=2)

        self.texto = Label(self.frame, text="COD. BARRA")
        self.texto.config(font=("Arial"))
        self.texto.grid(row=1, column=0, sticky="e")

        self.cod_barra = Entry(self.frame)
        self.cod_barra.grid(row=1, column=1, sticky="w")

        self.texto = Label(self.frame, text="CANTIDAD")
        self.texto.config(font=("Arial"))
        self.texto.grid(row=2, column=0, sticky="e")

        self.cantidad = Entry(self.frame)
        self.cantidad.insert(0,"1")
        self.cantidad.grid(row=2, column=1, sticky="w")
        
        self.agregar = Button(self.frame, text="Agregar", command=self.agregar)
        self.agregar.grid(row=5, column=0, sticky="e")
        
        self.limpiar = Button(self.frame, text="Limpiar", command=self.limpiar)
        self.limpiar.grid(row=5, column=1, sticky="w")
        
        self.tree = ttk.Treeview(self.frame, height = 15, columns=("producto", "precio", "cantidad","subtotal"))
        self.tree.heading("#0", text="Id Venta")
        self.tree.heading("#1", text="Producto")
        self.tree.heading("#2", text="Precio")
        self.tree.heading("#3", text="Cantidad")
        self.tree.heading("#4", text="SubTotal")
        self.tree.grid(row=7, column=0, columnspan=3, padx=5, pady=10)
        
        verscrlbar = ttk.Scrollbar(self.frame,orient ="vertical",command = self.tree.yview)
        verscrlbar.grid(column=3, row=7, sticky='w')
        self.tree.configure(xscrollcommand = verscrlbar.set)
        
        self.eliminar = Button(self.frame, text="Eliminar", command=self.eliminar)
        self.eliminar.grid(row=16, column=2, columnspan=2)
        
        self.texto = Label(self.frame, text="TOTAL")
        self.texto.config(font=("Arial",14))
        self.texto.grid(row=18, column=0, sticky="e", pady=10)
               
        self.venta = Button(self.frame, text="VENDER", command=self.vender)
        self.venta.grid(row=19, column=0, columnspan=2, pady=10)
        self.venta.config(font=("Arial", 18))
        
        self.lebel_total = tk.Entry(self.frame)
        self.lebel_total.config(font=("Arial", 12))
        self.lebel_total.grid(row=18, column=1, sticky="w", pady=10)
        
        self.traer_ventas()
        self.sumar()
               
    def show(self):
        sql = '''
            SELECT 
                producto_id,
                nombre,
                precio
            FROM 
                productos
            WHERE producto_id = ?
        '''
        params = (self.cod_barra.get(),)
        product = execute_query(sql, params)
        
        barra=product[0][0]
        
        prod=[product[0][1]]
       
        precio=[product[0][2]]
        
        canti=[self.cantidad.get()]
        
        subtotal=[self.tree_subtotal]
        
        self.tree.insert("", END,text=barra, 
                                values=(prod,
                                        precio,
                                        canti,
                                        subtotal))
        self.sumar()
        self.traer_ventas()
            
        
                             
    def agregar(self):
        
        if self.cod_barra.get() == '' or self.cantidad.get() == '':
            messagebox.showerror("Error", "Todos los campos son requeridos.")
        else:
            cantidad=self.cantidad.get()
            id_prod=self.cod_barra.get()
            sql = execute_query ("SELECT nombre, stock FROM productos WHERE producto_id = ?",id_prod)
            producto=sql[0][0]
            stock_db=sql[0][1]
            if int(stock_db) < int(cantidad):
                messagebox.showerror("Error", f"No hay stock suficiente. Quedan {stock_db} de {producto}")
            else:
                self.producto= detalle_producto(self.cod_barra.get())
                sql = "INSERT INTO ventas(producto, precio, cantidad, subtotal) VALUES(?, ?, ?, ?)"
                cantidad= int(self.cantidad.get())
                precio=float(self.producto[0][2])
                subtotal = cantidad * precio
                params = (self.producto[0][1],precio, cantidad, subtotal)
                execute_query(sql, params)
                
                self.tree_subtotal=float(subtotal)
                self.traer_ventas()
                self.actualizar_stock()
                self.cod_barra.delete(0, END)
                self.sumar()    
            
    def actualizar_stock(self):
        cantidad= self.cantidad.get()
        id_prod= self.cod_barra.get()
       
        sql = "SELECT stock FROM productos WHERE producto_id = ?"
        params= execute_query(sql,id_prod)
        stock_db=params[0][0]
       
        act_stock=int(stock_db)-int(cantidad)
        
        sql2 = "UPDATE productos SET stock = ? WHERE producto_id = ?"
        params2 = (act_stock,id_prod)
        execute_query(sql2, params2)
                
    def traer_ventas(self):
        
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        
        sql = "SELECT * FROM ventas WHERE cerrada = 0 ORDER BY venta_id DESC"
        product = execute_query(sql)
        
        for row in product:
            self.tree.insert('', 0, text = row[0], values = (row[1], row[2], row[3], row[4]))
            self.tree.cget
        
        
    def sumar(self):
        self.total=0
        
        for i in self.tree.get_children():
            try:
                self.total += float(self.tree.item(i)['values'][3])
            except:
                pass
        self.lebel_total.delete(0, tk.END)
        self.lebel_total.insert(0, self.total)       
        
    def eliminar(self):
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            messagebox.showerror("Error", "Seleccione un registro.")
            return
        
        product=(self.tree.item(self.tree.selection())['values'][0],)
        item=(self.tree.item(self.tree.selection())['text'],)
        result = messagebox.askquestion("Borrar", "¿Desea eliminar {} este registro?".format(product), icon="warning")
        if result == 'yes':
            sql = "DELETE FROM ventas WHERE venta_id = ?"
            params = item
            execute_query(sql, params)
            messagebox.showinfo("Bien", "Venta eliminada correctamente.")
        self.traer_ventas()
   
    def limpiar(self):
        self.cod_barra.delete(0, END)
        
    def vender(self):
        
        total=self.total
        sql_ventas="SELECT venta_id FROM ventas WHERE cerrada = 0 ORDER BY venta_id ASC"
        id_venta=execute_query(sql_ventas)
        datos=''
        for row in id_venta:
            i=row
            for x in range(len(i)):
                datos=f'{datos}/{str(i[x])}'
        #print(datos)
               
        sql = "INSERT INTO reportes(detalle, fecha, hora, total) VALUES(?, ?, ?, ?)"
        params=(datos,datetime.now().strftime("%d/%m/%Y"), datetime.now().strftime("%H:%M"),total)
        execute_query(sql,params)
   
        sql = "UPDATE ventas SET cerrada = 1 WHERE cerrada = 0"
        execute_query(sql)
        self.traer_ventas()           

class Reportes:
    def __init__(self, master):
        self.master = master
        self.master.title("Reportes")
        self.master.geometry("11900x600")
        self.frame = Frame(self.master)
        self.frame.pack()

        self.texto = Label(self.frame, text="REPORTES")
        self.texto.config(font=("Arial",16))
        self.texto.grid(row=0, column=0, columnspan=2)

        self.texto = Label(self.frame, text="Buscar por Día")
        self.texto.config(font=("Arial"))
        self.texto.grid(row=1, column=0, sticky="e")

        self.dia = Entry(self.frame)
        self.dia.grid(row=1, column=1, sticky="w")
        self.limpia = Button(self.frame, text="Borrar busqueda", command=self.limpiar)
        self.limpia.grid(row=4, column=0, pady=5, sticky="e")

        self.busqueda = Button(self.frame, text="Buscar", command=self.buscar)
        self.busqueda.grid(row=4, column=1, pady=5, sticky="w")

        self.tree = ttk.Treeview(self.frame, height = 15, columns=("id", "detalle", "dia", "hora"))
        self.tree.heading("#0", text="ID Ventas")
        self.tree.heading("#1", text="Detalle")
        self.tree.heading("#2", text="Dia")
        self.tree.heading("#3", text="Hora")
        self.tree.heading("#4", text="Total")
        self.tree.grid(row=7, column=0, columnspan=2, padx=5, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.selected_item)
        self.show()
        
        verscrlbar = ttk.Scrollbar(self.frame,orient ="vertical",command = self.tree.yview)
        verscrlbar.grid(column=2, row=7, sticky='w')
        self.tree.configure(xscrollcommand = verscrlbar.set)
        
        self.eliminar = Button(self.frame, text="Eliminar", command=self.eliminar)
        self.eliminar.grid(row=16, column=0, pady=5, sticky="e")
        
        self.actualizar = Button(self.frame, text="Ver Detalle de venta", command=self.detalle_venta)
        self.actualizar.grid(row=16, column=1, pady=5, sticky="w")
        
        self.show()

    def show(self):
        self.tree.delete(*self.tree.get_children())
        sql = "SELECT * FROM reportes ORDER BY reporte_id DESC"
        rows = execute_query(sql)
        for row in rows:
            self.tree.insert("", END, text=row[0], values=(row[1], row[2], row[3], row[4]))

    
    def buscar(self):
        if self.dia.get() == '':
            messagebox.showerror("Error", "Ingrese una fecha.")
        else:
            try:
                sql = "SELECT * FROM reportes WHERE fecha = ?"
                params = (self.dia.get(),)

                self.tree.delete(*self.tree.get_children())
                rows = execute_query(sql,params)
                for row in rows:
                    self.tree.insert("", END, text=row[0], values=(row[1], row[2], row[3], row[4]))
            except:
                 messagebox.showerror("Error", "No hubo ventas el {}.".format(self.dia.get()))
           
            
    def eliminar(self):
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            messagebox.showerror("Error", "Seleccione un registro.")
            return
        
        dia=(self.tree.item(self.tree.selection())['values'][1],)
        hora=(self.tree.item(self.tree.selection())['values'][2],)
        item=(self.tree.item(self.tree.selection())['text'],)
        result = messagebox.askquestion("Borrar", "¿Desea eliminar la venta del {} a las {} del registro?".format(dia,hora), icon="warning")
        if result == 'yes':
            sql = "DELETE FROM reportes WHERE reporte_id = ?"
            params = item
            execute_query(sql, params)
            messagebox.showinfo("Bien", "Reporte eliminado correctamente.")
        self.show()

    def detalle_venta(self):
        detalle_ventana = Toplevel(padx=15,pady=15)
        detalle_ventana.title ('Detalle de Venta')
        
        tree = ttk.Treeview(detalle_ventana, height = 15, columns=("producto", "precio", "cantidad","subtotal"))
        tree.heading("#0", text="Id Venta")
        tree.heading("#1", text="Producto")
        tree.heading("#2", text="Precio")
        tree.heading("#3", text="Cantidad")
        tree.heading("#4", text="SubTotal")
        tree.grid(row=4, column=0, columnspan=3, padx=5, pady=10)
        
        verscrlbar = ttk.Scrollbar(detalle_ventana,orient ="vertical",command = self.tree.yview)
        verscrlbar.grid(column=3, row=4, sticky='w')
        tree.configure(xscrollcommand = verscrlbar.set)
        
        texto = Label(detalle_ventana, text="TOTAL")
        texto.config(font=("Arial",14))
        texto.grid(row=18, column=2, sticky="e", pady=5)
        total = tk.Entry(detalle_ventana,textvariable = StringVar(self.frame, value = self.tree.item(self.tree.selection())['values'][3]))
        total.config(font=("Arial", 20))
        total.grid(row=19, column=2, sticky="e", pady=5)
                
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            messagebox.showerror("Error", "Seleccione un registro.")
            return
        params = []
        dato = self.tree.item(self.tree.selection())['values'][0]
        id_venta = dato.split('/')
        del id_venta[0]
        for x in id_venta:
            #x=int(x)
            params.append(x)
        params = tuple(params)
        for id in params:
            param=(id,)
            sql = "SELECT venta_id, producto, precio, cantidad, subtotal FROM ventas WHERE venta_id = ?"
            detalle = execute_query(sql,param)
            for row in detalle:
                tree.insert("", END, text=row[0], values=(row[1], row[2], row[3], row[4]))
            
                        
    def selected_item(self, event):
        curItem = self.tree.focus()
        contents = (self.tree.item(curItem))
        selected_item = contents['values']
        self.dia.delete(0, END)
        self.dia.insert(0, selected_item[1])
       

    def limpiar(self):
        self.dia.delete(0, END)
        self.show()


class MenuPrincipal:
    def __init__(self, master):
        self.master = master
        self.master.title("Menu Principal")
        self.master.geometry("900x500")
        #self.master.configure(background="grey")
        self.frame = Frame(self.master)
        self.frame.pack()

        self.texto = Label(self.frame, text="MENU PRINCIPAL")
        self.texto.config(font=("Arial", 36))
        self.texto.grid(row=0, column=0, columnspan=2, pady=20)

        self.boton_productos = Button(self.frame, font=("Arial", 20), text="Productos", command=self.productos)
        self.boton_productos.grid(row=1, column=0, padx=5, pady=20)

        self.boton_ventas = Button(self.frame, font=("Arial", 20), text="Ventas", command=self.ventas)
        self.boton_ventas.grid(row=2, column=0, padx=5, pady=20)

        self.boton_reportes = Button(self.frame, font=("Arial", 20), text="Reportes", command=self.reportes)
        self.boton_reportes.grid(row=3, column=0, padx=5, pady=20)

    def productos(self):
        self.newWindow = Toplevel(self.master)
        self.app = Productos(self.newWindow)

    def ventas(self):
        self.newWindow = Toplevel(self.master)
        self.app = Ventas(self.newWindow)

    def reportes(self):
        self.newWindow = Toplevel(self.master)
        self.app = Reportes(self.newWindow)


if __name__ == "__main__":
    root = Tk()
    menu = MenuPrincipal(root)
    root.mainloop()