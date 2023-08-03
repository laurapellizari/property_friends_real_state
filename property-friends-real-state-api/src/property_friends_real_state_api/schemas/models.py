from pydantic import BaseModel

class HealthSchema(BaseModel):
    api_up: bool
    api_version: str
    message: str

class InputFeatures(BaseModel):
    type: str
    sector: str
    net_usable_area: float
    net_area: float
    n_rooms: float
    n_bathroom: float
    latitude: float
    longitude: float
    price: float