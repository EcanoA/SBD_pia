import tkinter as tk
from tkinter import messagebox
import pyodbc
import logging 

def conexion():
    server = 'localhost'
    bd = 'BOLETERIA'
    usuario = 'CODIGO'
    contrasena = '123'

    print("Intentando conexion...")
    logging.info("Intentando conexion a base de datos...")

    try:
        conexion  = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL server}; SERVER='
                                    +server+';DATABASE='+bd+';UID='+usuario+';PWD='+contrasena)

        print("...Conexion exitosa")
        logging.info("...Conexion exitosa")

    except Exception as e:
        print("...Fallo al intentar conexion")
        logging.error("Ha ocurrido un error al intentar la conexion: " + str(e))

        quit()

def salir():
    vprincipal.destroy()


##### Logging #####
# Configuracion
logging.basicConfig(filename='App.log', 
                    level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s', 
                    datefmt='%m/%d/%Y %I:%M:%S %p')


##### Ventana #####
# Configuracion ventana principal
vprincipal = tk.Tk()
vprincipal.title("Menu Boleteria")
vprincipal.geometry("225x180")
vprincipal.configure(background='gray')


##### Botones #####
# Configuraciones
boton1 = tk.Button(vprincipal, 
                    text = "Agregar boleto")

boton2 = tk.Button(vprincipal, 
                    text = "Agregar evento")

boton3 = tk.Button(vprincipal, 
                    text = "Consultar boleto")

boton4 = tk.Button(vprincipal, 
                    text = "Consultar eventos")

botonsalir = tk.Button(vprincipal, 
                        text = "Salir" ,
                        fg = 'Black', 
                        command = salir)

# Agregando botones
boton1.pack()
boton2.pack()
boton3.pack()
boton4.pack()
botonsalir.pack()


if __name__ == '__main__':
    conexion()
    vprincipal.mainloop()