from DB.conexion import Base #importamos base desde el módulo conexion para poder definir las clases modelo para interactuar con la base de datos
from sqlalchemy import Column, Integer, String #importamos colum, interger y string

class User(Base):
    __tablename__ = 'tbUsers' #nombre de la tabla
    #columnas de la tabla con sus propiedades
    id = Column(Integer, primary_key=True, autoincrement= "auto")
    name = Column(String)
    age = Column(Integer)
    email = Column(String)