from fastapi.responses import JSONResponse
from modelsPydantic import modelAuth #importar las model
from genToken import createToken #importar las genToken
from fastapi import APIRouter

routerAuth = APIRouter()

#ENDPOINT PARA GENERAR TOKEN
@routerAuth.post('/auth', tags = ['Autentificación']) #CREACIÓN DEL POST PARA GENERAR TOKEN
def auth(credenciales: modelAuth):  #DEFINICIÓN DE LAS CREDENCIALES
    if credenciales.mail == 'kmaria.grosales@gmail.com' and credenciales.passw == '123456789': #SE CREA UN USUARIO ESTÁTICO CON UNA CONTRASEÑA ESTÁTICA
        token:str = createToken(credenciales.model_dump()) #SI LAS CREDENCIALES SON VÁLIDAS SE GENERA UN TOKEN USANDO LA FUNCIÓN createToken Y LOS DATOS PROPORCIONADOS EN credenciales
        print(token) #IMPRIME EL TOKEN EN LA CONSOLA
        return JSONResponse(content = token) #SE DEVUELVE LA RESPUESTA JSON CON EL CONTENIDO DEL TOKEN
    else:
        return {"AVISO": "USUARIO NO CUENTA CON LAS CREDENCIALLES"} #SI LAS CREDENCIALES NO SON VÁLIDAS, SE DEVUELVE UN MENSAJE DE AVISO INDICANDO QUE EL USUARIO NO TIENE CREDENCIALES VÁLIDAS