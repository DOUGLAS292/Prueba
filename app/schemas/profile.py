# from pydantic import BaseModel, EmailStr
# from typing import Optional
# from datetime import datetime


# # --- Modelo base de perfil ---
# class ProfileBase(BaseModel):
#     full_name: str
#     role: str = "client"
#     profession: Optional[str] = None
#     city: Optional[str] = None
#     country: Optional[str] = None
#     bio: Optional[str] = None
#     experience_years: int = 0
#     phone: Optional[str] = None
#     image_url: Optional[str] = None
#     rating_avg: float = 0.0
#     rating_count: int = 0


# # --- Modelo para creación de perfil ---
# class ProfileCreate(ProfileBase):
#     email: EmailStr               # para registrar usuario en Supabase Auth
#     password: str                 # contraseña para Supabase Auth


# # --- Modelo de respuesta de perfil ---
# class ProfileResponse(ProfileBase):
#     id: str                       # UUID de Supabase Auth
#     created_at: Optional[datetime] = None

#     class Config:
#         from_attributes = True


from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --------------------------
# BASE
# --------------------------
class ProfileBase(BaseModel):
    email: str                   # 👈 AGREGAR ESTO
    password: str
    full_name: str
    role: str = "client"
    profession: Optional[str] = None
    city: Optional[str] = None
    bio: Optional[str] = None
    experience_years: int = 0
    phone: Optional[str] = None
    image_url: Optional[str] = None
    rating_avg: float = 0.0
    rating_count: int = 0


# --------------------------
# CREACIÓN
# --------------------------
class ProfileCreate(ProfileBase):
    password: str  # usado solo al crear el usuario

# --------------------------
# RESPUESTA (para devolver datos al frontend)
# --------------------------
class ProfileResponse(ProfileBase):
    id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --------------------------
# PERFIL GENERAL (alias)
# --------------------------
Profile = ProfileResponse  # 🔥 esto permite que otros módulos sigan importando "Profile"
