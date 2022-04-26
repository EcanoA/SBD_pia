# Codigo en esp evitando palabras/signos no dispoibles en ingles
# Usar pep8 de preferencia
# La funcion para cerrar cada ventana se define debajo del boton

##### Importaciones #####

import tkinter as tk
from tkinter import messagebox
import pyodbc
import logging 

##### Funciones #####
# Funcion para conectar con base de datos
def conexion():
    server = 'localhost'
    bd = 'BOLETERIA'
    usuario = 'CODIGO'
    contrasena = '123'

    logging.info("Intentando conexion a base de datos...")

    try:
        conexion  = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL server}; SERVER='
                                    +server+';DATABASE='+bd+';UID='+usuario+';PWD='+contrasena)

        logging.info("...Conexion exitosa")

    except Exception as e:
        logging.error("Ha ocurrido un error al intentar la conexion: " + str(e))

        #quit()


##### Ventanas extras #####
# Ventana para agregar boletos
def v_agregarboletos():
    logging.info("Abriendo ventana agregar boletos")

    # Configuracion
    v_agregar1 = tk.Toplevel(vprincipal)
    v_agregar1.title("Agregar Boletos")
    v_agregar1.geometry("550x500")
    v_agregar1.configure(background = 'purple')

    # Botones



# Ventana para agregar eventos
def v_agregareventos():
    logging.info("Abriendo ventana agregar eventos")

    # Configuracion
    v_agregar2 = tk.Toplevel(vprincipal)
    v_agregar2.title("Agregar Eventos")
    v_agregar2.geometry("550x500")
    v_agregar2.configure(background = 'blue')

    # Botones



# Ventana para consultar boletos
def v_consultarboletos():
    logging.info("Abriendo ventana consultar boletos")

    # Configuracion
    v_agregar3 = tk.Toplevel(vprincipal)
    v_agregar3.title("Consultar Boletos ")
    v_agregar3.geometry("550x500")
    v_agregar3.configure(background = 'black')

    # Botones



# Ventana para cosultar eventos
def v_consultareventos():
    logging.info("Abriendo ventana cosultar eventos")

    # Configuracion
    v_agregar1 = tk.Toplevel(vprincipal)
    v_agregar1.title("Cosultar Eventos")
    v_agregar1.geometry("550x500")
    v_agregar1.configure(background = 'cyan')

    # Botones

# Cerrar ventana
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
vprincipal.geometry("225x240")
vprincipal.configure(background='gray')

# Label para que se vea bonito <3
label1 = tk.Label(vprincipal, 
                    text = "Boleteria FCFM",
                    justify = 'center',
                    anchor = 'center')
label1.configure(font = '{TkFixedFont} 18 {}')

##### Botones #####
# Configuraciones
boton1 = tk.Button(vprincipal, 
                    text = "Agregar boleto",
                    command = v_agregarboletos,
                    justify = 'center')

boton2 = tk.Button(vprincipal, 
                    text = "Agregar evento", 
                    command = v_agregareventos)

boton3 = tk.Button(vprincipal, 
                    text = "Consultar boleto", 
                    command = v_consultarboletos)

boton4 = tk.Button(vprincipal, 
                    text = "Consultar eventos", 
                    command = v_consultareventos)

botonsalir = tk.Button(vprincipal, 
                        text = "Salir",
                        command = salir)

# Agregando botones
label1.pack(anchor='center', 
            expand='true', 
            fill='x', 
            ipady='0', 
            side='top')
boton1.pack(pady = '5')
boton2.pack(pady = '5')
boton3.pack(pady = '5')
boton4.pack(pady = '5')
botonsalir.pack(pady = '5')


if __name__ == '__main__':
    logging.info("Programa iniciado...")
    conexion()
    vprincipal.mainloop()