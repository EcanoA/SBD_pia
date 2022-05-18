# Codigo en esp evitando palabras/signos no dispoibles en ingles
# Usar pep8 de preferencia
# Para los botones de ventanas extras se usa una nomenclatura antes de cada boton 
# Ejemplo: ab_btn1 <- agregar boleto boton 1
# debido a que no se construyo con clases las funciones necesarias para cada ventana estan
# dentro de cada funcion de la propia ventana
# cada funcion de consulta o agregado tiene que conectarse      

##### Importaciones #####
import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc
import logging 

##### Ventanas extras #####
# Ventana para agregar boletos
def v_agregarboletos():
    logging.info("Abriendo ventana agregar boletos")

    # Configuracion
    v_agregar1 = tk.Toplevel(vprincipal)
    v_agregar1.title("Agregar Boletos")
    v_agregar1.geometry("600x500")
    v_agregar1.configure(background = 'purple')

    # Botones
    ag_btn1 = tk.Button(v_agregar1, text = "Agregar boleto")
    agb_ent1 = tk.Entry(v_agregar1)
    agb_ent2 = tk.Entry(v_agregar1)
    agb_ent3 = tk.Entry(v_agregar1)
    agb_ent4 = tk.Entry(v_agregar1)
    agb_ent5 = tk.Entry(v_agregar1)
    prueba = ttk.Combobox(v_agregar1,
                        state = "readonly",
                        values = ["prueba","Prueba2"])

    prueba.pack()

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

    # Funcion para consulta de los boletos
    def consultaboletos():
        boletoid = str(cb_ent2.get())
        apellido = str(cb_ent1.get())

        if boletoid == "" or apellido == "":
            messagebox.showwarning("Error","No se dieron los argumentos requeridos")
            return

        # valores necesarios
        server = 'localhost'
        bd = 'BOLETERIA'
        usuario = 'CODIGO'
        contrasena = '123'

        logging.info("Intentando conexion a base de datos...")

        # haciendo conexion
        try:
            conexion  = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL server}; SERVER='
                                        +server+';DATABASE='+bd+';UID='+usuario+';PWD='+contrasena)

            logging.info("...Conexion exitosa")

        except Exception as e:
            logging.error("Ha ocurrido un error al intentar la conexion: " + str(e))
            quit()

        # valores necesarios para la consulta y la consulta
        cursor = conexion.cursor()

        consulta = """declare @idboleto int
        set @idboleto = @x
        declare @apellido varchar(50)
        set @apellido = '@y'
        SELECT B.idBoleto,E.nombre as Evento, C.Apellido, L.AsientoNum, L.ZonaNom, E.fecha, Loc.Ciudad, Loc.Estado
        FROM Boleto B
        left join Evento E
        ON E.idEvento = B.idEvento
        left join Comprador C
        ON C.idComprador = B.idComprador
        left join 
        (
        	SELECT L2.idLugar,L2.idZona,Z.ZonaNom,L2.AsientoNum
        	FROM Lugar L2
        	left join Zona Z
        	ON L2.idZona = Z.idZona
        )L
        ON B.idLugar = L.idLugar
        left join Localidad Loc
        ON B.idLocalidad = Loc.idLocalidad
        where B.idBoleto =  @idboleto and C.Apellido = @apellido"""
        consulta = consulta.replace("@x",boletoid)
        consulta = consulta.replace("@y",apellido)

        try:    

            cursor.execute(consulta)
            filas = cursor.fetchone() # traer resultados
        except:
            logging.error("Ha ocurrido un error al consultar boletos")
            print("algo va mal")
            quit()

        # imprimir resultados
        if filas == None:
            filas = "No coinciden las busquedas con ningun boleto registrado"
            messagebox.showinfo("Boleto",filas)
        else:
            mensaje = """   ID Boleto: @idboleto
    Nombre: @nombre
    Evento: @evento
    Zona: @zona
    Asiento: @asiento
    Fecha: @fecha
    Lugar: @municipio, @estado"""
            mensaje = mensaje.replace("@idboleto",str(filas[0]))
            mensaje = mensaje.replace("@evento",str(filas[1]))
            mensaje = mensaje.replace("@nombre",str(filas[2]))
            mensaje = mensaje.replace("@zona",str(filas[4]))
            mensaje = mensaje.replace("@asiento",str(filas[3]))
            mensaje = mensaje.replace("@fecha",str(filas[5]))
            mensaje = mensaje.replace("@municipio",str(filas[6]))
            mensaje = mensaje.replace("@estado",str(filas[7]))
            messagebox.showinfo("Info Boleto",mensaje)

        
    ## Definicion ventana ##
    logging.info("Abriendo ventana consultar boletos")

    # Configuracion
    v_consultar1 = tk.Toplevel(vprincipal)
    v_consultar1.title("Consultar Boletos ")
    v_consultar1.geometry("554x306")

    # Botones
    cb_ent2 = tk.Entry(v_consultar1)
    cb_label2 = tk.Label(v_consultar1, 
                        text = "Id del boleto", )
    cb_ent1 = tk.Entry(v_consultar1)
    cb_label1 = tk.Label(v_consultar1, 
                        text = "Apellido registrado en el boleto", )
    cb_btn1 = tk.Button(v_consultar1, text = "Consultar",command=consultaboletos)

    cb_label2.place(x=90,y=50,width=156,height=30)
    cb_ent2.place(x=290,y=50,width=70,height=25)
    cb_label1.place(x=90,y=90,width=170,height=30)
    cb_ent1.place(x=290,y=90,width=70,height=25)
    cb_btn1.place(x=350,y=230,width=156,height=30)

# Ventana para cosultar eventos
def v_consultareventos():
    
    # Funcion para consulta de los boletos
    def consultaeventos():
        # valores necesarios
        server = 'localhost'
        bd = 'BOLETERIA'
        usuario = 'CODIGO'
        contrasena = '123'

        logging.info("Intentando conexion a base de datos...")

        # haciendo conexion
        try:
            conexion  = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL server}; SERVER='
                                        +server+';DATABASE='+bd+';UID='+usuario+';PWD='+contrasena)

            logging.info("...Conexion exitosa")

        except Exception as e:
            logging.error("Ha ocurrido un error al intentar la conexion: " + str(e))
            quit()

        # valores necesarios para la consulta y la consulta
        cursor = conexion.cursor()

        consulta = """declare @date varchar(50)
        Set @date =GETDATE()
        SELECT Ev.nombre, TE.TipoEvento, Ev.fecha, D.Disponibilidad, L.Ciudad, L.Estado, L.Pais
        FROM Evento Ev
        left join TipoEvento TE
        ON Ev.idTipoEvento = TE.idTipoEvento
        left join Disponibilidad D
        ON Ev.idEvento = D.idEvento
        left join Localidad L
        ON Ev.idLocalidad = L.idLocalidad
        where Ev.fecha >= @date"""
        cursor.execute(consulta)
        filas = cursor.fetchall() # traer resultados
        print(filas)

        # imprimir resultados
        for fila in filas:
            print("Evento",filas)

    ## Definicion ventana ##
    logging.info("Abriendo ventana cosultar eventos")

    # Configuracion
    v_consultar2 = tk.Toplevel(vprincipal)
    v_consultar2.title("Cosultar Eventos")
    v_consultar2.geometry("550x500")
    v_consultar2.configure(background = 'cyan')

    # Botones
    ce_btn1 = tk.Button(v_consultar2, text = "Consultar eventos disponibles",
                        command=consultaeventos)
    ce_btn1.place(x=360,y=340,width=156,height=30)

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
    vprincipal.mainloop()




