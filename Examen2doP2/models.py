from pydantic import BaseModel, Field
class modelVehiculo(BaseModel):
    id: int = Field(...,gt = 0, description = "SOLO SE ACEPTAN VALORES MAYORES A 0")
    año: int = Field(..., ge = 2000, le = 2025, description = "SOLO SE ACEPTAN DE 20 A 25 CARACTERES")
    modelo: str = Field(..., min_length = 4, max_length = 25, description = "SOLO SE ACEPTAN DE 4 A 25 CARACTERES")
    placa: str = Field(..., min_length = 6, max_length = 10, description = "SOLO SE ACEPTAN DE 6 A 10 CARACTERES")