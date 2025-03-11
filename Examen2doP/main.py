from fastapi import FastAPI, HTTPException #Importar la clase FastAPI, HTTPException  y Depends
from fastapi.responses import JSONResponse
from typing import Optional, List #Importar los tipos de datos Optional y List

app = FastAPI(
    title = "Examen"
) #Instancia de la clase FastAPI

vehiculos = [
    {"id": 1, "modelo": "Audi", "año": "2021", "placa": "UMZ234S"},
    {"id": 2, "modelo": "Toyota", "año": "2020", "placa": "UMZ234S"},
    {"id": 3, "modelo": "Mazda", "año": "2019", "placa": "UMZ234S"}
]

@app.get()

@app.post("/registro/", tags = ["REGISTRO"])
def guardar(registro: dict): 
    for registro in registro: 
        if registro["id"] == registro.get("id"):
            raise HTTPException(status_code=400, detail="El vehiculo ya existe")
    vehiculos.append(registro)
    return registro

#endpoint para buscar un vehiculo por placa
@app.get("/vehiculos/{placa}", tags = ["VEHICULOS"])

def leer(placa: str):
    for vehiculo in vehiculos:
        if vehiculo["placa"] == placa:
            return vehiculo
    raise HTTPException(status_code=404, detail="Vehiculo no encontrado")

#endpoint para obtener todos los vehículos
@app.get("/vehiculos/", tags = ["VEHICULOS"])
def leerTodos():
    return vehiculos