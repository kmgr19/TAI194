from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from genToken import validateToken

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)

        if not isinstance(data, dict): #verificar si es un diccionario válido
            raise HTTPException(status_code = 401, detail = 'Formato de token no válido')
        
        if data.get('mail') != 'kmaria.grosales@gmail.com': #usar .get()para evitar KeyError
            raise HTTPException(status_code = 403, detail = 'Credenciales no validadas')
        return data