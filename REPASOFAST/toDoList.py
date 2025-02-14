from fastapi import FastAPI, HTTPException #Importar la clase FastAPI
from typing import Optional #Sirve para poder hacer los parámetros opcionales

app = FastAPI(
    title = "Repaso fastAPI",
    desription = "García Rosales Karla María",
    version = "1.0.0"
) #MANDAR AL CONSTRUCTOR QUE QUEREMOS QUE TENGA ESTE OBJETO CUSNDO SE INICIE, TODO SE HARÁ A TRAVÉS DE ESE OBJETO

tareas = [
    {"id":1, "tarea":"Hacer tarea de matemáticas", "estado":"pendiente"},
    {"id":2, "tarea":"Hacer tarea de español", "estado":"pendiente"},
    {"id":3, "tarea":"Hacer tarea de historia", "estado":"pendiente"},
    {"id":4, "tarea":"Hacer tarea de inglés", "estado":"pendiente"},
    {"id":5, "tarea":"Hacer tarea de ciencias", "estado":"pendiente"},
    {"id":6, "tarea":"Hacer tarea de educación física", "estado":"pendiente"},
    {"id":7, "tarea":"Hacer tarea de artes", "estado":"pendiente"},
]

#CREAR PRIMERA RUTA O ENDPOINT
app.get("/", tags = ["inicio"]) #declarar ruta del servidor
def home():
    return {'BIENVENIDO': 'TAREAS'} #mensaje que se mpstrará en la ruta del servidor

@app.get("/tareas", tags = ["tareas"]) #declarar ruta del servidor
def leer():
    return {'Tareas Registradas: ': tareas} #se concatenan las tareas registradas

#ENDPOINT POST
@app.post("/tareas/", tags = ["TAREAS"]) #declarar ruta del servidor
def guardar(tarea: dict): #recibe un objeto tipo dict
    for tarea in tarea: 
        if tarea["id"] == tarea.get("id"): 
            raise HTTPException(status_code=400, detail="La tarea ya existe") #si el id ya existe se manda un mensaje de error
    tarea.append(tarea) #se agrega la tarea a la lista
    return tarea #mensaje de tarea agregada

#ENDPOINT ACTUALIZAR
@app.put("/tareas/{id}", tags = ["TAREAS"]) #declarar ruta del servidor
def actualizar(id: int, tareaActualizada: dict): #recibe un objeto tipo dict
    for index, tarea in enumerate(tareas): #se recorre la lista de tareas y se enumeran para saber la posición
        if tarea["id"] == id: #se verifica que el id coincida en el parámetro
            tareas[index].update(tareaActualizada) #se actualiza la tarea
            return tarea[index] #se regresa la tarea actualizada
    raise HTTPException(status_code = 404, detail = "La tarea no existe") #si no se encuentra la tarea se manda un mensaje de error

#ENDPOINT DELETE
@app.delete("/tareas/", tags = ["TAREAS"]) #declarar ruta del servidor
def delete(id: int, tareaEliminada: dict): #se utiliza el parámetro obligatorio y el diccionario que se va a actualizar que en este caso es la tarea
    for index, tarea in enumerate(tareas):
        if tarea["id"] == id: #se verifica que el id coincida en el parámetro
            del tareas[index] #se elimina la tarea
            return {"mensaje": "Tarea eliminada"} #se regresa el mensaje de tarea eliminada
    raise HTTPException(status_code = 404, detail = "La tarea no existe") #te manda un mensaje en caso de que no se encuentre la tarea o ya se ha eliminado
            