from pydantic import BaseModel, Field
class modelVehiculo(BaseModel):
    año: int
    modelo: str = Field(..., min_length = 4, max_length = 25, description = "SOLO SE ACEPTAN DE 4 A 25 CARACTERES")
    placa: str = Field(..., min_length = 6, max_length = 10, description = "SOLO SE ACEPTAN DE 6 A 10 CARACTERES")