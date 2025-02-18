from fastapi import FastAPI, HTTPException #Importar la clase FastAPI
from typing import Optional #Sirve para poder hacer los parámetros opcionales

app = FastAPI(
    title = "Repaso fastAPI",
    desription = "García Rosales Karla María",
    version = "1.0.0"
) #MANDAR AL CONSTRUCTOR QUE QUEREMOS QUE TENGA ESTE OBJETO CUSNDO SE INICIE, TODO SE HARÁ A TRAVÉS DE ESE OBJETO

tareas = [
    {"id":1, "título":"Desarrollar una aplicación móvil", "descripción":"Crear una aplicación para gestión de calificaciones", "vencimiento": "17-02-2025", "estado":"pendiente"},
    {"id":2, "título":"Desarrollar una base de datos", "descripción":"Crear y mejorar la estructura de una BD", "vencimiento": "24-02-2025", "estado":"pendiente"},
    {"id":3, "título":"Implementación de diseño", "descripción":"Implementar el diseño de la aplicación", "vencimiento": "03-03-2025", "estado":"pendiente"},
    {"id":4, "título":"Desarrollar una api", "descripción":"Desarrollar una api que tenga funciones de un CRUD", "vencimiento": "13-03-2025", "estado":"pendiente"},
    {"id":5, "título":"Subir al repositorio", "descripción":"Subir la aplicación en un repositorio", "vencimiento": "17-03-2025", "estado":"pendiente"},
]

#ENDPOINT CONSULTA TODOS
@app.get("/tareas", tags = ["TAREAS"]) #declarar ruta del servidor
def leer():
    return {'Tareas Registradas: ': tareas} #se concatenan las tareas registradas

@app.post("/tareas/", tags = ["TAREAS"])#declarar ruta del servidor
def guardar(tareacreada: dict): #se recibe un diccionario, después de los : es el tipo de dato que se está solicitando
    for task in tareas: #recorrer la lista de tareas
        if task["id"] == tareacreada.get("id"): #si es igual al tarea de la petición
            raise HTTPException(status_code=400, detail="El tarea ya existe") #raise: marca un punto de quiebre, el status code se refiere a un error en específico
    tareas.append(tareacreada) #agregar el tarea a la lista
    return tareacreada #mensaje de tarea agregada

#ENDPOINT ACTUALIZAR
@app.put("/tareas/{id}", tags = ["TAREAS"]) #declarar ruta del servidor
def actualizar(id:int, tareaActualizada:dict): #recibe un objeto tipo dict
    for index, task in enumerate(tareas): #se recorre la lista de tareas y se enumeran para saber la posición
        if task["id"] == id: #se verifica que el id coincida en el parámetro
            tareas[index].update(tareaActualizada) #se actualiza la tarea
            return tareas[index] #se regresa la tarea actualizada
    raise HTTPException(status_code = 404, detail = "La tarea no existe") #si no se encuentra la tarea se manda un mensaje de error

#ENDPOINT DELETE
@app.delete("/tareas/{id}", tags = ["TAREAS"]) #declarar ruta del servidor
def delete(id: int): #recibe un objeto tipo dict
    print(f"solicitud delete {id}")
    for index, task in enumerate(tareas): #se recorre la lista de tareas y se enumeran para saber la posición
        if task["id"] == id: #se verifica que el id coincida en el parámetro
            del tareas[index] #se elimina la tarea
            print(f"tarea con id {id} eliminada")
            return {"mensaje": "tarea eliminada"} #se regresa un mensaje de tarea eliminada
    print(f"tarea con id {id} no encontrada")
    raise HTTPException(status_code = 404, detail = "La tarea no existe") #si no se encuentra la tarea se manda un mensaje de error