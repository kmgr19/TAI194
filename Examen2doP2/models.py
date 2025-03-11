from pydantic import BaseModel, Field
class modelVehiculo(BaseModel):
    id: int = Field(...,min_length = 1, max_length = 10, description = "SOLO SE ACEPTAN DE 1 A 10 CARACTERES")
    marca: str = Field(..., min_length = 3, max_length = 25, description = "SOLO SE ACEPTAN DE 3 A 25 CARACTERES")
    año: int = Field(..., min_length = 20, max_length = 25, description = "SOLO SE ACEPTAN DE 20 A 25 CARACTERES")
    modelo: str = Field(..., min_length = 4, max_length = 25, description = "SOLO SE ACEPTAN DE 4 A 25 CARACTERES")
    placa: str = Field(..., min_length = 6, max_length = 10, description = "SOLO SE ACEPTAN DE 6 A 10 CARACTERES")