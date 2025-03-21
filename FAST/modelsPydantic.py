from pydantic import BaseModel, Field, EmailStr 

class modelUsuario(BaseModel): #se crea una clase que hereda de BaseModel
    name: str = Field(..., min_length = 1, max_length = 85, description = "Solo letras y espacios, min 1 y max 85") # se hacen validaciones para solo aceptar nmbres solo con letras y espacios con un mínimo y máximo de caracteres
    age: int = Field(..., ge = 0, le = 120 , description = "Solo se aceptan edades desde 0 a 120") #se hacen validaciones para solo aceptar edades desde 0 a 120
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$', description="Debe ser un correo válido")

class modelAuth(BaseModel):
    mail: EmailStr
    passw: str = Field(..., min_length=8, strip_whitespace = True, description = "solo letras sin espacios, min 8 caracteres")