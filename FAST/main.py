from fastapi import FastAPI

app = FastAPI()

#ruta o EndPoint
@app.get('/')
def home():
    return {'hello': 'world fastApi'}

#EndPoint promedio
@app.get('/promedio')
def promedio():
    return 10.5

#EndPoint con parámetro obligatorio
@app.get('/usuario/{id}')
def consultausuario(id:int):
    #caso ficticio de búsqueda en BD
    return {"Se encontró el usuario":id}