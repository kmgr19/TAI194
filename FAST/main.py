from fastapi import FastAPI, HTTPException #Importar la clase FastAPI
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

#ENDPOINT CONSULTA TODOS
@app.get("/todosUsuarios", tags = ["Operaciones CRUD"])#declarar ruta del servidor
def leer():
    return {'Usuarios Registrados: ': usuarios} #se concatenan los ususarios registrados

#ENDPOINT POST
@app.post("/usuarios/", tags = ["Operaciones CRUD"])#declarar ruta del servidor
def guardar(usuario: dict): #se recibe un diccionario, después de los : es el tipo de dato que se está solicitando
    for usr in usuarios: #recorrer la lista de usuarios
        if usr["id"] == usuario.get("id"): #si es igual al usuario de la petición
            raise HTTPException(status_code=400, detail="El usuario ya existe") #raise: marca un punto de quiebre, el status code se refiere a un error en específico

    usuarios.append(usuario) #agregar el usuario a la lista
    return usuario #mensaje de usuario agregado    

#ENDPOINT ACTUALIZAR
@app.put("/usuarios/{id}", tags = ["Operaciones CRUD"]) #{} es un parámetro obligatorio que en este caso es el id
def actualizar(id:int, usuarioActualizado: dict): #se utiliza el parámetro obligatorio y el diccionario que se va a actualizar que en este caso es el usuario
    for index, usr in enumerate(usuarios): #se recorre la lista de usuarios y se enumeran para saber la posición en la que se encuentran
        if usr["id"] == id: #se verifica que el id coincida en el parámetro
            usuarios[index].update(usuarioActualizado) #se actualiza el usuario
            return usuarios[index] #se regresa el usuario actualizado
    raise HTTPException(status_code = 404, detail = "El usuario no existe") #si no se encuentra el usuario se manda un mensaje de error    

#ENDPOINT DELETE
@app.delete("/usuarios/", tags = ["Operaciones CRUD"]) #DECLARAR LA RUTA DEL SERVIDOR
def delete(id:int, usuarioEliminado: dict): #se utiliza el parámetro obligatorio y el diccionario que se va a actualizar que en este caso es el usuario
    for index, usr in enumerate(usuarios): #se recorre la lista de usuarios y se enumeran para saber la posición
        if usr["id"] == id: #se verifica que el id coincida en el parámetro
            del usuarios[index] #se elimina el usuario
            return {"mensaje": "Usuario eliminado"} #se regresa el mensaje de usuario eliminado
    raise HTTPException(status_code = 404, detail = "El usuario no existe") #te manda un mensaje en caso de que no se encuentre el ususario o ya se ha eliminado       