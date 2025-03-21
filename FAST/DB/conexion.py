import os #importamos el módulo os para interactuar con el sistema operativo
from sqlalchemy import create_engine #establece la conexión con la base de datos
from sqlalchemy.orm.session import sessionmaker #crea la sesión con la base de datos
from sqlalchemy.ext.declarative import declarative_base #clases modelo que representan tablas en la base de datos

dbName = 'usuarios.sqlite' #nombre de la base de datos
base_dir = os.path.dirname(os.path.realpath(__file__)) #obtemenos el directorio base del archivo actual
dbURL = f"sqlite:///{os.path.join(base_dir, dbName)}" #URL de conexión para la base de datos

#motor que se conectará con la base de datos
engine = create_engine(dbURL, echo = True) #True habilitará el modo de depuración para mostrar los comandos SQL generados
Session = sessionmaker(bind=engine) #permite interactuar con la base de datos a través de sesiones
Base = declarative_base() #clase base para las clases modelo que representan las tablas