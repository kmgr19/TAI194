from fastapi import FastAPI, HTTPException, Depends #Importar la clase FastAPI, HTTPException  y Depends
from fastapi.responses import JSONResponse
from typing import Optional, List #Importar los tipos de datos Optional y List
from models import modelUsuario, modelAuth #importar las model
from genToken import createToken #importar las genToken
from middlewares import BearerJWT # importar las middlewares

app = FastAPI(
    title = "Mi primer API",
    description = "García Rosales Karla María",
    version = "1.0.0"
) #MANDAR AL CONSTRUCTOR QUE QUEREMOS QUE TENGA ESTE OBJETO CUSNDO SE INICIE, TODO SE HARÁ A TRAVÉS DE ESE OBJETO

usuarios = [ #se crea una lista de usuarios
    {"id":1, "nombre":"Karla", "edad":20, "correo":"karla@gmail.com"}, 
    {"id":2, "nombre":"María", "edad":20, "correo":"maria@gmail.com"},
    {"id":3, "nombre":"Dora", "edad":22, "correo":"dora@gmail.com"},
    {"id":4, "nombre":"Andrea", "edad":22, "correo":"andrea@gmail.com"},
]

#CREAR PRIMERA RUTA O ENDPOINT
@app.get("/", tags = ["inicio"])#declarar ruta del servidor
def home():
    return {'hello': 'world fastApi'} #mensaje que se mpstrará en la ruta del servidor

#ENDPOINT PARA GENERAR TOKEN
@app.post('/auth', tags = ['Autentificación']) #CREACIÓN DEL POST PARA GENERAR TOKEN
def auth(credenciales: modelAuth):  #DEFINICIÓN DE LAS CREDENCIALES
    if credenciales.mail == 'kmaria.grosales@gmail.com' and credenciales.passw == '123456789': #SE CREA UN USUARIO ESTÁTICO CON UNA CONTRASEÑA ESTÁTICA
        token:str = createToken(credenciales.model_dump()) 
        print(token)
        return JSONResponse(content = token)
    else:
        return {"AVISO": "USUARIO NO CUENTA CON LAS CREDENCIALLES"}    

#ENDPOINT CONSULTA TODOS
@app.get("/todosUsuarios/", response_model = List[modelUsuario], tags = ["Operaciones CRUD"]) #declarar ruta del servidor
def leer(token: dict = Depends(BearerJWT())):
    print ("aviso", token)
    return usuarios #se regresa la lista de usuarios

#ENDPOINT POST
@app.post("/usuarios/",  response_model = modelUsuario, tags = ["Operaciones CRUD"]) #declarar ruta del servidor
def guardar(usuario: modelUsuario): #se recibe un objeto usando la clase modelUsuario  
    for usr in usuarios: #recorrer la lista de usuarios
        if usr["id"] == usuario.id: #si es igual al usuario de la petición 
            raise HTTPException(status_code=400, detail="El usuario ya existe") #raise: marca un punto de quiebre, el status code se refiere a un error en específico

    usuarios.append(usuario) #agregar el usuario a la lista
    return usuario #mensaje de usuario agregado    

#ENDPOINT ACTUALIZAR
@app.put("/usuarios/{id}", response_model= modelUsuario, tags = ["Operaciones CRUD"]) #{} es un parámetro obligatorio que en este caso es el id
def actualizar(id:int, usuarioActualizado: modelUsuario): #se utiliza el parámetro obligatorio y el diccionario que se va a actualizar que en este caso es el usuario
    for index, usr in enumerate(usuarios): #se recorre la lista de usuarios y se enumeran para saber la posición en la que se encuentran
        if usr["id"] == id: #se verifica que el id coincida en el parámetro
            usuarios[index] = usuarioActualizado.model_dump() #se actualiza el usuario
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