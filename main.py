# El codigo esta escrito es español evitando letras o caracteres no disponibles en ingles

# Importaciones
import pyodbc
import logging

# Funcion para conexion con base de datos
def conexion ():
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



# Iniciando log 
logging.basicConfig(filename='App.log', 
                    level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s', 
                    datefmt='%m/%d/%Y %I:%M:%S %p')

# Metodo main
if __name__=="__main__":
    # Intentando la conexion
    conexion()