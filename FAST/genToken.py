import jwt

def createToken(data: dict): #función que recibe un diccionario
    token: str = jwt.encode(payload = data, key = 'secretkey', algorithm = 'HS256') 
    return token #regresa el token
