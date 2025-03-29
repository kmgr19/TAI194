from fastapi import FastAPI #Importar la clase FastAPI
from DB.conexion import engine, Base #importar las clases de la base de datos
from routers.usuarios import routerUsuario
from routers.auth import routerAuth

app = FastAPI(
    title = "Mi primer API",
    description = "García Rosales Karla María",
    version = "1.0.0"
) #MANDAR AL CONSTRUCTOR QUE QUEREMOS QUE TENGA ESTE OBJETO CUSNDO SE INICIE, TODO SE HARÁ A TRAVÉS DE ESE OBJETO

Base.metadata.create_all(bind = engine) #CREAR LAS TABLAS EN LA BASE DE DATOS

#CREAR PRIMERA RUTA O ENDPOINT
@app.get("/", tags = ["inicio"])#declarar ruta del servidor
def home():
    return {'hello': 'world fastApi'} #mensaje que se mostrará en la ruta del servidor

app.include_router(routerUsuario)
app.include_router(routerAuth)