import jwt
from jwt import ExpiredSignatureError, InvalidTokenError #CLASES DE VALIDACIONES DE ERRORES
from fastapi import HTTPException

def createToken(data: dict): #función que recibe un diccionario
    token: str = jwt.encode(payload = data, key = 'secretkey', algorithm = 'HS256') 
    return token #regresa el token

def validateToken(token:str): #validación del token (forzosamente una cadena)
    try:
        data:dict = jwt.decode(token, key = 'secretkey', algorithms = ['HS256']) #se comprueba si está bien el token, se pone como algorithms porque se pueden pasar muchos como una lista
        return data
    
    except ExpiredSignatureError:
        raise HTTPException(status_code = 404, detail = 'TOKEN EXPIRADO') #VALIDACIÓN SI EL TOKEN YA CADUCÓ

    except InvalidTokenError: 
        raise HTTPException(status_code = 404, detail = 'TOKEN NO AUTORIZADO') #VALIDACIÓN SI EL TOKEN NO SE AUTORIZÓ
    