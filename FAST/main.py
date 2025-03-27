from fastapi import FastAPI, HTTPException, Depends #Importar la clase FastAPI, HTTPException  y Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Optional, List #Importar los tipos de datos Optional y List
from modelsPydantic import modelUsuario, modelAuth #importar las model
from genToken import createToken #importar las genToken
from middlewares import BearerJWT # importar las middlewares
from DB.conexion import Session, engine, Base #importar las clases de la base de datos
from models.modelsDB import User #importar la clase User

app = FastAPI(
    title = "Mi primer API",
    description = "García Rosales Karla María",
    version = "1.0.0"
) #MANDAR AL CONSTRUCTOR QUE QUEREMOS QUE TENGA ESTE OBJETO CUSNDO SE INICIE, TODO SE HARÁ A TRAVÉS DE ESE OBJETO

Base.metadata.create_all(bind = engine) #CREAR LAS TABLAS EN LA BASE DE DATOS

usuarios = [ #se crea una lista de usuarios
    {"id":1, "nombre":"Karla", "edad":20, "correo":"karla@gmail.com"}, 
    {"id":2, "nombre":"María", "edad":20, "correo":"maria@gmail.com"},
    {"id":3, "nombre":"Dora", "edad":22, "correo":"dora@gmail.com"},
    {"id":4, "nombre":"Andrea", "edad":22, "correo":"andrea@gmail.com"},
]

#CREAR PRIMERA RUTA O ENDPOINT
@app.get("/", tags = ["inicio"])#declarar ruta del servidor
def home():
    return {'hello': 'world fastApi'} #mensaje que se mostrará en la ruta del servidor

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
@app.get("/todosUsuarios/", tags = ["Operaciones CRUD"]) #Declara la ruta del servidor para realizar la operación de obtener todos los usuarios
def leer(): #Define la función que se encargará de recuperar todos los usuarios registrados en la base de datos
    db = Session() #Crea una nueva sesión con la base de datos para interactuar con ella
    try:
        consulta = db.query(User).all() #Realiza una consulta en la base de datos para obtener todos los registros de la tabla `User`
        return JSONResponse(content = jsonable_encoder(consulta)) #Devuelve una respuesta JSON con los datos de todos los usuarios, codificados correctamente para JSON
    
    except Exception as e: #Bloque para manejar errores que puedan ocurrir durante la operación de consulta
        db.rollback() #Revierte cualquier cambio realizado en la sesión en caso de que ocurra un error
        return JSONResponse(status_code = 500, content = {"message": "NO FUE POSIBLE CONSULTAR", "Error": str(e)}) #Devuelve una respuesta JSON con un código de estado HTTP 500 y un mensaje de error indicando que ocurrió un problema

    finally:  
        db.close() # Cierra la conexión con la base de datos, independientemente de si hubo éxito o error en la consulta.

#ENDPOINT CONSULTA POR ID
@app.get("/usuario/{id}", tags = ["Operaciones CRUD"]) #declarar ruta del servidor
def leeruno(id:int): #define la función que recibe como parámetro el id del usuario
    db = Session() #crea una nueva sesión con la base de datos
    try:
        consulta1 = db.query(User).filter(User.id == id).first() #realiza una consulta en la base de datos para obtener el usuario cuyo id coincida con el parámetro 'id'
        if not consulta1: #verifica si el usuario no fue encontrado
            return JSONResponse(status_code = 404, content = {"mensaje": "USUARIO NO ENCONTRADO"})  #Devuelve una respuesta JSON con un código de estado HTTP 404 y un mensaje indicando que el usuario no fue encontrado
        
        return JSONResponse(content = jsonable_encoder(consulta1)) #Devuelve una respuesta JSON con los datos del usuario encontrado, codificados correctamente para JSON
    
    except Exception as e: #Bloque para manejar errores que puedan ocurrir durante la consulta a la base de datos
        db.rollback()
        return JSONResponse(status_code = 500, content = {"message": "NO FUE POSIBLE CONSULTAR", "Error": str(e)}) #se regresa un mensaje de error en caso de que no se haya guardado el usuario

    finally:  
        db.close() #se cierra la conexión con la base de datos 

#ENDPOINT POST
@app.post("/usuarios/",  response_model = modelUsuario, tags = ["Operaciones CRUD"]) #declarar ruta del servidor
def guardar(usuario: modelUsuario): #se recibe un objeto usando la clase modelUsuario  
    db = Session()
    try: 
        db.add(User(**usuario.model_dump())) #se agrega el usuario a la base de datos
        db.commit() #se guardan los cambios
        return JSONResponse(status_code = 201, content = {"message": "Usuario guardado", "usuario": usuario.model_dump()}) #se regresa un mensaje de usuario guardado

    except Exception as e: #error en la base de datos
        db.rollback()
        return JSONResponse(status_code = 500, content = {"message": "ERROR: Usuario no guardado", "Error": str(e)}) #se regresa un mensaje de error en caso de que no se haya guardado el usuario

    finally:  
        db.close() #se cierra la conexión con la base de datos 

#ENDPOINT PARA ACTUALIZAR
@app.put('/Usuarios/{id}', response_model=modelUsuario, tags=['Operaciones CRUD'])
def actualizar(id: int, usuarioActualizado: modelUsuario):
    db = Session()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="El usuario no existe")
        
        for key, value in usuarioActualizado.model_dump().items():
            setattr(usuario, key, value)
        
        db.commit()
        return usuarioActualizado.model_dump()

    except Exception as e:
        db.rollback() 
        return JSONResponse(status_code=500, content={"message": "No fue posible actualizar el usuario", "Error": str(e)})
    
    finally:
        db.close()

#ENDPOINT PARA BORRAR
@app.delete('/Usuarios/{id}', tags=['Operaciones CRUD'])
def eliminar(id: int):
    db = Session()
    try:
        
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="El usuario no existe")
        
        db.delete(usuario)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Usuario eliminado exitosamente"})

    except Exception as e:
        db.rollback()  
        return JSONResponse(status_code=500, content={"message": "No fue posible eliminar el usuario", "Error": str(e)})
    
    finally:
        db.close()