# No se usan letras o signos no existentes en el ingles 

from distutils.util import execute
import pyodbc

# Datos para conexion
server = 'localhost'
bd = 'BOLETERIA'
usuario = 'CODIGO'
contrasena = '123'


try:

    conexion  = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL server}; SERVER='
        +server+';DATABASE='+bd+';UID='+usuario+';PWD='+contrasena)

    print("Conexion exitosa")
    
    print("Uniendo datos")

    cursorInsert = conexion.cursor()

    consulta = "Insert into Comprador(Nombre,Apellido) values('Prueba', 'Pruebas');"
    cursorInsert.execute(consulta)

    cursorInsert.commit()
    cursorInsert.close()

    print("Datos agregados")

except:
    print("Error al intentar conectarse")


