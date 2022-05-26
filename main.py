# Codigo en esp evitando palabras/signos no dispoibles en ingles
# Usar pep8 de preferencia
# Para los botones de ventanas extras se usa una nomenclatura antes de cada boton 
# Ejemplo: ab_btn1 <- agregar boleto boton 1
# debido a que no se construyo con clases las funciones necesarias para cada ventana estan
# dentro de cada funcion de la propia ventana
# cada funcion de consulta o agregado tiene que conectarse      

##### Importaciones #####

import re
import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc
import logging 
from datetime import datetime

##### Ventanas extras #####
# Ventana para agregar boletos
def v_agregarboletos():
    def agregarboletos():
        try:
            evento = ent1.get()
            filtro = '(\W{1,})(\w{1,}|\w{1,}\w{1,}|\w{1,}\w{1,}\w{1,})(\W{1,})'
            buscar = re.search(filtro,evento)
            evento = buscar.group(2)
            nombre = str(ent2.get())
            apellido = ent3.get()
            zona = str(ent5.get())
            buscar = re.search(filtro,zona)
            zona = buscar.group(2)
            tipopago = str(ent4.get())
            buscar = re.search(filtro,tipopago)
            tipopago = buscar.group(2)
            numasientos = 1
            asiento = str(ent7.get())
        except Exception as e:
            logging.error("Ha ocurrido un error 1: " + str(e))
            messagebox.showerror("Error","No se otorgaron los datos necesarios")
            quit()
        
        #obtener id evento
        cursor = conexion.cursor()
        consulta = "SELECT idEvento FROM Evento where nombre = '@evento'"
        consulta = consulta.replace("@evento",evento)
        cursor.execute(consulta)
        idevento = str(cursor.fetchone())
        filtro = '(\W{1,})(\d{1,})(\W{1,})'
        buscar = re.search(filtro,idevento)
        idevento = buscar.group(2)
        cursor.close()

        #Agregar comprador
        cursor = conexion.cursor()
        consulta = "INSERT INTO Comprador(Nombre,Apellido) values('@nombre','@apellido')"
        consulta = consulta.replace("@nombre",nombre)
        consulta = consulta.replace("@apellido",apellido)
        cursor.execute(consulta)
        cursor.commit()

        #obtener id comprador
        cursor = conexion.cursor()
        consulta = "SELECT idComprador FROM Comprador where Nombre = '@nombre' and Apellido = '@apellido'"
        consulta = consulta.replace("@nombre",nombre)
        consulta = consulta.replace("@apellido",apellido)
        cursor.execute(consulta)
        idcomprador = str(cursor.fetchone())
        filtro = '(\W{1,})(\d{1,})(\W{1,})'
        buscar = re.search(filtro,idcomprador)
        idcomprador = buscar.group(2)
        cursor.close()

        #obtener idzona
        cursor = conexion.cursor()
        consulta = "SELECT idZona FROM Zona where ZonaNom = '@zona'"
        consulta = consulta.replace("@zona",zona)
        cursor.execute(consulta)
        idzona = str(cursor.fetchone())
        filtro = '(\W{1,})(\d{1,})(\W{1,})'
        buscar = re.search(filtro,idzona)
        idzona = buscar.group(2)
        cursor.close()

        #obtener disponibilidad
        cursor = conexion.cursor()
        consulta = "SELECT Disponibilidad FROM Disponibilidad where idEvento = @idevento and idZona = @idzona"
        consulta = consulta.replace("@idevento",idevento)
        consulta = consulta.replace("@idzona",idzona)
        cursor.execute(consulta)
        disponibilidad = str(cursor.fetchone())
        filtro = '(\W{1,})(\d{1,})(\W{1,})'
        buscar = re.search(filtro,disponibilidad)
        disponibilidad = buscar.group(2)
        cursor.close()

        #agregar asientos
        cursor = conexion.cursor()
        consulta = "INSERT INTO Lugar(AsientoNum,idZona) values(@asiento,@idzona);"
        consulta = consulta.replace("@asiento",asiento)
        consulta = consulta.replace("@idzona",idzona)
        cursor.execute(consulta)
        cursor.commit()
        cursor.close()
        
        #consultar asiento
        cursor = conexion.cursor()
        consulta = "SELECT idLugar FROM Lugar where AsientoNum = @asiento and idZona = @idZona"
        consulta = consulta.replace("@asiento",asiento)
        consulta = consulta.replace("@idZona",idzona)
        cursor.execute(consulta)
        idasiento = str(cursor.fetchone())
        filtro = '(\W{1,})(\d{1,})(\W{1,})'
        buscar = re.search(filtro,idasiento)
        idasiento = buscar.group(2)
        cursor.close()

        #consultar localidad
        cursor = conexion.cursor()
        consulta = "SELECT idLocalidad FROM Evento where idEvento = @idevento"
        consulta = consulta.replace("@idevento",idevento)
        cursor.execute(consulta)
        idlocalidad = str(cursor.fetchone())
        filtro = '(\W{1,})(\d{1,})(\W{1,})'
        buscar = re.search(filtro,idlocalidad)
        idlocalidad = buscar.group(2)
        cursor.close()

        #obtener fecha pago 
        fechapago = str(datetime.today().strftime('%d/%m/%Y'))

        #Agregar boleto
        cursor = conexion.cursor()
        consulta = "INSERT INTO Boleto(idEvento, idComprador, idLugar, idLocalidad, fechapago) values(@idevento,@idcomprador,@idlugar,@idlocalidad,@fechapago)"
        consulta = consulta.replace("@idevento",idevento)
        consulta = consulta.replace("@idcomprador",idcomprador)
        consulta = consulta.replace("@idlugar",idasiento)
        consulta = consulta.replace("@idlocalidad",idlocalidad)
        consulta = consulta.replace("@fechapago",fechapago)
        cursor.execute(consulta)
        cursor.commit()
        cursor.close()

        if disponibilidad is None:
            messagebox.showerror("Error","No se puede completar la compra")

        nuevadis = int(disponibilidad) - int(numasientos)
        nuevadis = str(nuevadis)
        if int(nuevadis) < 0:
            messagebox.showerror("Error","No se puede completar la compra")
        #actualizar disponibilidad
        cursor = conexion.cursor()
        consulta = "UPDATE Disponibilidad SET Disponibilidad = @nuevadis WHERE idZona = @idzona and idEvento = @idevento"
        consulta = consulta.replace("@nuevadis",nuevadis)
        consulta = consulta.replace("@idzona",idzona)
        consulta = consulta.replace("@idevento",idevento)
        cursor.execute(consulta)
        cursor.commit()

        #costo
        cursor = conexion.cursor()
        consulta = "SELECT Precio FROM Precio WHERE idEvento = @idevento and idZona = @idzona"
        consulta = consulta.replace("@idzona",idzona)
        consulta = consulta.replace("@idevento",idevento)
        cursor.execute(consulta)
        precio = str(cursor.fetchone())
        filtro = '(\W{1,})(\d{1,})(\W{1,})'
        buscar = re.search(filtro,precio)
        precio = buscar.group(2)      

        costo = precio * numasientos
        messagebox.showinfo("Costo","Compra realizada con exito, se realizo un cargo de $"+costo) 

        f=open("Boleto.txt","w")
        boletocompleto="""Nombre: @evento
        zona: @zona
        asiento: @asiento
        apellido: @apellido"""
        boletocompleto = boletocompleto.replace("@evento",evento)
        boletocompleto = boletocompleto.replace("@zona",zona)
        boletocompleto = boletocompleto.replace("@asiento",asiento)
        boletocompleto = boletocompleto.replace("@apellido",apellido)
        f.write(boletocompleto)
        f.close()



    logging.info("Abriendo ventana agregar boletos")

    # Configuracion
    server = 'localhost'
    bd = 'BOLETERIA'
    usuario = 'CODIGO'
    contrasena = '123'
    logging.info("Intentando conexion a base de datos...")
    try:
        conexion  = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL server}; SERVER='
                                    +server+';DATABASE='+bd+';UID='+usuario+';PWD='+contrasena)
        logging.info("...Conexion exitosa")
        cursor = conexion.cursor()
        consulta = "SELECT nombre FROM Evento"
        cursor.execute(consulta)
        eventos = cursor.fetchall()

        consulta = "SELECT ZonaNom FROM Zona"
        cursor.execute(consulta)
        zonas = cursor.fetchall()

        consulta = "SELECT TipoPago FROM FormaPago"
        cursor.execute(consulta)
        formaspago = cursor.fetchall()
        cursor.close()
    except Exception as e:
        logging.error("Ha ocurrido un error al intentar la conexion: " + str(e))
        quit()


    v_agregar1 = tk.Toplevel(vprincipal)
    v_agregar1.title("Agregar Boletos")
    v_agregar1.geometry("600x500")

    # Botones
    lb1 = tk.Label(v_agregar1,text="Evento")
    lb2 = tk.Label(v_agregar1,text="Nombre")
    lb3 = tk.Label(v_agregar1,text="Apellido")
    lb4 = tk.Label(v_agregar1,text="Forma Pago")
    lb5 = tk.Label(v_agregar1,text="Zona")
    lb7 = tk.Label(v_agregar1, text="Asiento")
    ent1 = ttk.Combobox(v_agregar1,values=eventos)
    ent2 = tk.Entry(v_agregar1)
    ent3 = tk.Entry(v_agregar1)
    ent4 = ttk.Combobox(v_agregar1,values=formaspago)
    ent5 = ttk.Combobox(v_agregar1,values=zonas)
    ent7 = tk.Entry(v_agregar1)

    lb1.place(x=30,y=20)
    lb2.place(x=30,y=60)
    lb3.place(x=30,y=100)
    lb4.place(x=30,y=270)
    lb5.place(x=30,y=160)
    ent1.place(x=150,y=20)
    ent2.place(x=150,y=60)
    ent3.place(x=150,y=100)
    ent4.place(x=150,y=270)
    ent5.place(x=150,y=160)
    lb7.place(x=300,y=160)
    ent7.place(x=430,y=160)
    
    btn1 = tk.Button(v_agregar1,command=agregarboletos,text="Agregar")
    btn1.place(x=470,y=430)



# falta terminar
# Ventana para agregar eventos
def v_agregareventos():

    def agregarevento():
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

        evento = str(ent1.get())
        fecha = str(ent3.get())
        tipoevento = str(ent2.get())
        filtro = '(\W{1,})(\w{1,}|\w{1,}\w{1,}|\w{1,}\w{1,}\w{1,})(\W{1,})'
        buscar = re.search(filtro,tipoevento)
        tipoevento = buscar.group(2)
        pais = str(ent4.get())
        estado = str(ent5.get())
        municipio = str(ent6.get())
        #agregar localidad y consultar id
        try:
            cursor = conexion.cursor()
            consulta = "INSERT INTO Localidad(Estado,Pais,Ciudad) values('@estado','@pais','@municipio');"
            consulta = consulta.replace("@estado",estado)
            consulta = consulta.replace("@pais",pais)
            consulta = consulta.replace("@municipio",municipio)
            cursor.execute(consulta)
            cursor.commit()

            consulta = "select idLocalidad from Localidad where pais = '@pais' and estado = '@estado' and Ciudad = '@municipio'"
            consulta = consulta.replace("@estado",estado)
            consulta = consulta.replace("@pais",pais)
            consulta = consulta.replace("@municipio",municipio)
            cursor.execute(consulta)
            idlocalidad = cursor.fetchone()
            cursor.close()
        except Exception as e:
            logging.error("Error al agregar datos",e)
            quit()

        #consultar tipo evento
        try:
            cursor = conexion.cursor()
            consulta = "select idTipoEvento from TipoEvento where TipoEvento = '@tipo'"
            consulta = consulta.replace("@tipo",tipoevento)
            cursor.execute(consulta)
            idtipoevento = cursor.fetchone()
            print(idevento)
        except Exception as e:
            logging.error("Error al agregar datos",e)


        #agregar evento y obtener id
        try:
            cursor = conexion.cursor()
            consulta = "INSERT INTO Evento(nombre,idTipoEvento,fecha,idLocalidad) values('@nombre',@idtipo,'@fecha',@idlocalidad);"
            consulta = consulta.replace("@nombre",evento)
            consulta = consulta.replace("@idtipo",idtipoevento)
            consulta = consulta.replace("@fecha",fecha)
            consulta = consulta.replace("@idlocalidad",idlocalidad)
            cursor.execute(consulta)
            cursor.commit()


            consulta = "select idEvento from Evento where nombre = @nombre and fecha = @fecha"
            consulta = consulta.replace("@nombre",evento)
            consulta = consulta.replace("@fecha",fecha)
            cursor.execute(consulta)
            idevento = cursor.fetchone() 
            
            cursor.close()
        except Exception as e:
            logging.error("Error al agregar datos",e)
        
    logging.info("Abriendo ventana agregar eventos")

    # Configuracion
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
        
        consulta = "select TipoEvento from TipoEvento"
        cursor = conexion.cursor()
        cursor.execute(consulta)
        seleccionar = cursor.fetchall()
    except Exception as e:
        logging.error("Ha ocurrido un error al intentar la conexion: " + str(e))
        quit()
    
    
    v_agregar2 = tk.Toplevel(vprincipal)
    v_agregar2.title("Agregar Eventos")
    v_agregar2.geometry("600x500")

    # Botones
    lb1 = tk.Label(v_agregar2, text="Nombre Evento")
    lb3 = tk.Label(v_agregar2, text="Fecha del Evento")
    lb2 = tk.Label(v_agregar2, text="Tipo de Evento")
    lb4 = tk.Label(v_agregar2, text="Pais")
    lb5 = tk.Label(v_agregar2, text="Estado")
    lb6 = tk.Label(v_agregar2, text="Municipio")

    ent1 = tk.Entry(v_agregar2)
    ent2 = ttk.Combobox(v_agregar2,state="readonly",values=seleccionar)
    ent3 = tk.Entry(v_agregar2)
    ent4 = tk.Entry(v_agregar2)
    ent5 = tk.Entry(v_agregar2)
    ent6 = tk.Entry(v_agregar2)

    lb1.place(x=30,y=20)
    lb2.place(x=30,y=60)
    lb3.place(x=30,y=100)
    lb4.place(x=30,y=160)
    lb5.place(x=30,y=200)
    lb6.place(x=30,y=240)

    ent1.place(x=130,y=20,width=193)
    ent2.place(x=130,y=60,width=193)
    ent3.place(x=130,y=100,width=193)
    ent4.place(x=130,y=160,width=193)
    ent5.place(x=130,y=200,width=193)
    ent6.place(x=130,y=240,width=193)

    lb10 = tk.Label(v_agregar2, text="Usar formato dd/mm/yyyy")
    lb10.place(x=390,y=100)

    btn1 = tk.Button(v_agregar2,text="Agregar",command=agregarevento)
    btn1.place(x=460,y=40)


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
            logging.info("Consultado base de datos...")
            cursor.execute(consulta)
            logging.info("...Base de datos consultada con exito")
            filas = cursor.fetchone() # traer resultados
        except:
            logging.error("Ha ocurrido un error al consultar boletos")
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
        fecha = datetime.today().strftime('%d/%m/%Y')
        eventos = list()

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

        consulta = """SELECT Ev.nombre, TE.TipoEvento, Ev.fecha, D.Disponibilidad, L.Ciudad, L.Estado, L.Pais
FROM Evento Ev
left join TipoEvento TE
ON Ev.idTipoEvento = TE.idTipoEvento
left join Disponibilidad D
ON Ev.idEvento = D.idEvento
left join Localidad L
ON Ev.idLocalidad = L.idLocalidad"""
        consulta = consulta.replace("@x",fecha)

        try:
            logging.info("Consultado base de datos...")
            cursor.execute(consulta)
            logging.info("...Base de datos consultada con exito")
            filas = cursor.fetchall() # traer resultados
        except:
            logging.error("Ha ocurrido un error consultando los boletos")
        if filas == None:
            messagebox.showinfo("Eventos registrados","No se tiene registro de ningun evento")
        else:
            # imprimir resultados
            for fila in filas:
                evento = """Nombre evento: @evento
Tipo de evento: @tipo 
Fecha del evento: @fecha
Disponibilidad: @dis
Lugar del evento: @municipio, @estado, @pais
\n"""
                evento = evento.replace("@evento",str(fila[0]))
                evento = evento.replace("@tipo",str(fila[1]))
                evento = evento.replace("@fecha",str(fila[2]))
                evento = evento.replace("@dis",str(fila[3]))
                evento = evento.replace("@municipio",str(fila[4]))
                evento = evento.replace("@estado",str(fila[5]))
                evento = evento.replace("@pais",str(fila[6]))

                eventos.append(evento)
                f = open("Eventos registrados.txt",'w')
            for i in eventos:
                f.write(i)
            f.close()
        messagebox.showinfo("Eventos registrados","Se han guardado los eventos activos en un documento con nombre Eventos registrados")

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
    ce_btn1.place(x=150,y=150,width=156,height=30)

 
# Cerrar ventana
def salir():
    logging.info("Terminando programa")
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
                    text = "Agregar evento")

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




