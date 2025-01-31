from fastapi import FastAPI
from typing import Optional #Sirve para poder hacer los parámetros opcionales

app = FastAPI(
    title = "Mi primer API",
    desription = "García Rosales Karla María",
    version = "1.0.0"
) #MANDAR AL CONSTRUCTOR QUE QUEREMOS QUE TENGA ESTE OBJETO CUSNDO SE INICIE, TODO SE HARÁ A TRAVÉS DE ESE OBJETO

usuarios = [
    {"id":1, "nombre":"Karla", "edad":20},
    {"id":2, "nombre":"María", "edad":20},
    {"id":3, "nombre":"Dora", "edad":22},
    {"id":4, "nombre":"Andrea", "edad":22},
]

#CREAR PRIMERA RUTA O ENDPOINT
@app.get("/", tags = ["inicio"])#declarar ruta del servidor


def home():
    return {'hello': 'world fastApi'} #mensaje que se mpstrará en la ruta del servidor

#segunda ruta o endpoint con parámetro
@app.get('/promedio', tags = ["Mi calificación TAI"]) #DECLARAR RUTA DEL SERVIDOR

def promedio(): #FUNCIÓN QUE SE EJECUTARÁ CUANDO SE ENTRE A LA RUTA
    return 10.5

#EndPoint con parámetro obligatorio, TERCER RUTA
@app.get('/usuario/{id}', tags = ["Parámetro obligatorio"]) #declarar la ruta del servidor

def consultausuario(id:int): #función que se ejcutará cuando se entre a la ruta
    #caso ficticio de búsqueda en BD
    return {"Se encontró el usuario":id}

#crear ruta con parámetro opcional
@app.get('/usuario2/', tags=['Enpoint o praámetro opcional']) #declarar la ruta del servidor, se quita el parámetro de {}

def consultausuario2(id: Optional[int] = None): #se validará cuando se encuentre la ruta
    if id is not None: #SE VALIDA SI VIENE EL ID
        for usuario in usuarios: #iteración dentro del for
            if usuario["id"] == id: #SE BUSCA EL ID Y SE REGRESA UN MENSAJE
                return {"mensaje":"Usuario encontrado", "El usuario es: ":usuario}
        return {"mensaje":f"No se encontró el id: {id}"} #SI NO SE ENCUENTRA EL ID        
    
    return {"mensaje":"No se proporcionó un id"} #SI NO SE PROPORCIONA UN ID

#endpoint con varios parametro opcionales
@app.get("/usuarios/", tags=["3 parámetros opcionales"])
async def consulta_usuarios(
    usuario_id: Optional[int] = None,
    nombre: Optional[str] = None,
    edad: Optional[int] = None
):
    resultados = []

    for usuario in usuarios:
        if (
            (usuario_id is None or usuario["id"] == usuario_id) and
            (nombre is None or usuario["nombre"].lower() == nombre.lower()) and
            (edad is None or usuario["edad"] == edad)
        ):
            resultados.append(usuario)

    if resultados:
        return {"usuarios_encontrados": resultados}
    else:
        return {"mensaje": "No se encontraron usuarios que coincidan con los parámetros proporcionados."}