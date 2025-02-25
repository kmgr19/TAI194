from pydantic import BaseModel, Field 

class modelUsuario(BaseModel): #se crea una clase que hereda de BaseModel
    id: int = Field(..., gt = 0, description = "Id siempre debe de ser positivo") # se crean validaciones para que la edad que ingresemos solo sean números positivos
    nombre: str = Field(..., min_length = 1, max_length = 85, description = "Solo letras y espacios, min 1 y max 85") # se hacen validaciones para solo aceptar nmbres solo con letras y espacios con un mínimo y máximo de caracteres
    edad: int = Field(..., min_length = 0, max_length = 120 , description = "Solo se aceptan edades desde 0 a 120") #se hacen validaciones para solo aceptar edades desde 0 a 120
    correo: str = Field(..., regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', description="Correo electrónico válido") # se hacen validaciones para aceptar el correo solo si está en el formato correcto
