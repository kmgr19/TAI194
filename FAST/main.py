from fastapi import FastAPI

app = FastAPI()

#ruta o EndPoint
@app.get('/')
def home():
    return {'hello': 'world fastApi'}