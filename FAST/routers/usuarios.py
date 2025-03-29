from fastapi import HTTPException #Importar la clase  HTTPException 
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from modelsPydantic import modelUsuario #importar las model
from middlewares import BearerJWT # importar las middlewares
from DB.conexion import Session #importar las clases de la base de datos
from models.modelsDB import User #importar la clase User
from fastapi import APIRouter

routerUsuario = APIRouter()

#ENDPOINT CONSULTA TODOS
@routerUsuario.get("/todosUsuarios/", tags = ["Operaciones CRUD"]) #Declara la ruta del servidor para realizar la operación de obtener todos los usuarios
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
@routerUsuario.get("/usuario/{id}", tags = ["Operaciones CRUD"]) #declarar ruta del servidor
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
@routerUsuario.post("/usuarios/",  response_model = modelUsuario, tags = ["Operaciones CRUD"]) #declarar ruta del servidor
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
@routerUsuario.put('/Usuarios/{id}', response_model=modelUsuario, tags=['Operaciones CRUD']) #DEFINE UNA RUTA TIPO PUT 
def actualizar(id: int, usuarioActualizado: modelUsuario): #RECIBEN COMO PARÁMETROS EL ID DEL USUARIO Y UN OBJETO CON DATOS ACTUALIZADOS
    db = Session() #CREA UNA NUEVA SESIÓN CON LA BASE DE DATOS
    try:
        usuario = db.query(User).filter(User.id == id).first() #BUSCA EL USUARIO EN LA BASE DE DATOS FILTRANDO POR EL ID PROPORCIONADO
        if not usuario:
            raise HTTPException(status_code=404, detail="El usuario no existe") #MENSAJE DE ERROR SI NO SE ENCUENTRA EL USUARIO
        
        for key, value in usuarioActualizado.model_dump().items(): #RECORRE LOS CAMPOS DEL OBJETO DE USUARIO ACTUALIZADO
            setattr(usuario, key, value) #ASIGNA CADA VALOR AL ATRIBUTO CORRESPONDIENTE DEL USUARIO EN LA BASE DE DATOS
        
        db.commit() #CONFIRMA LOS CAMBIOS EN LA BASE DE DATOS
        return usuarioActualizado.model_dump() #DEVUELVE EL OBJETO ACTUALIZADO COMO RESPUESTA

    except Exception as e: #MANEJO DE EXCEPCIONES EN CASO DE ERROR
        db.rollback() #REVERSIÓN DE CAMBIOS EN CASO DE ERROR
        return JSONResponse(status_code=500, content={"message": "No fue posible actualizar el usuario", "Error": str(e)}) #MENSAJE DE ERROR EN CASO DE QUE NO SE HAYA PODIDO ACTUALIZAR EL USUARIO
    
    finally: 
        db.close() #CERRAR LA CONEXIÓN CON LA BASE DE DATOS

#ENDPOINT PARA BORRAR
@routerUsuario.delete('/Usuarios/{id}', tags=['Operaciones CRUD']) #DEFINE UNA RUTA TIPO DELETE
def eliminar(id: int): #RECIBE COMO PARÁMETRO EL ID DEL USUARIO A BORRAR
    db = Session() #CREA UNA NUEVA SESIÓN CON LA BASE DE DATOS
    try:
        
        usuario = db.query(User).filter(User.id == id).first() #BUSCA EL USUARIO EN LA BASE DE DATOS FILTRANDO POR EL ID PROPORCIONADO
        if not usuario: #VERIFICA SI EL USUARIO NO EXISTE
            raise HTTPException(status_code=404, detail="El usuario no existe") #MENSAJE DE ERROR SI NO SE ENCUENTRA EL USUARIO
        
        db.delete(usuario) #ELIMINA EL USUARIO DE LA BASE DE DATOS
        db.commit() #CONFIRMA LOS CAMBIOS EN LA BASE DE DATOS
        return JSONResponse(status_code=200, content={"message": "Usuario eliminado exitosamente"}) #MENSAJE DE ÉXITO EN CASO DE QUE SE HAYA PODIDO ELIMINAR EL USUARIO

    except Exception as e: #MANEJO DE EXCEPCIONES EN CASO DE ERROR
        db.rollback() #REVERSIÓN DE CAMBIOS EN CASO DE ERROR
        return JSONResponse(status_code=500, content={"message": "No fue posible eliminar el usuario", "Error": str(e)}) #MENSAJE DE ERROR EN CASO DE QUE NO SE HAYA PODIDO ELIMINAR EL USUARIO
    
    finally: 
        db.close() #CERRAR LA CONEXIÓN CON LA BASE DE DATOS