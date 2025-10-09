# from pydantic import BaseModel
# from typing import Optional

# class OfferBase(BaseModel):
#     title: str
#     description: Optional[str] = None
#     area_m2: Optional[float] = None
#     budget_cop: Optional[int] = None
#     # location as WKT string: "SRID=4326;POINT(lon lat)"
#     location: Optional[str] = None

# class OfferCreate(OfferBase):
#     client_id: str

# class OfferResponse(OfferBase):
#     id: int
#     client_id: str
#     status: Optional[str] = None
#     created_at: Optional[str] = None

#     class Config:
#         orm_mode = True

from pydantic import BaseModel
from typing import Optional, Union, Dict, Any


class OfferBase(BaseModel):
    """
    Modelo base para las ofertas.
    Acepta el campo location como string WKT (ej: 'SRID=4326;POINT(-74.0628 4.6486)')
    o como objeto GeoJSON (ej: {'type': 'Point', 'coordinates': [-74.0628, 4.6486]}).
    """
    title: str
    description: Optional[str] = None
    area_m2: Optional[float] = None
    budget_cop: Optional[int] = None
    location: Optional[Union[str, Dict[str, Any]]] = None  # Puede ser texto o JSON Geo


class OfferCreate(OfferBase):
    """
    Modelo para crear una oferta (request body).
    """
    client_id: str


class OfferResponse(OfferBase):
    """
    Modelo de respuesta para devolver los datos de una oferta.
    """
    id: int
    client_id: str
    status: Optional[str] = None
    created_at: Optional[str] = None
    location: Optional[Union[str, Dict[str, Any]]] = None

    class Config:
        # Pydantic v2 usa `from_attributes` en lugar de `orm_mode`
        from_attributes = True
