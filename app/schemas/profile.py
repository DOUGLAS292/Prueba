from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union
from datetime import datetime


class Profile(BaseModel):
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
    location: Optional[Union[str, Dict[str, Any]]] = None
    # created_at: datetime

# class ProfileCreate(ProfileBase):
#     id: str  # UUID del auth.user

# class Profile(ProfileBase):
#     id: str
#     rating_avg: float = 0.0
#     rating_count: int = 0
#     created_at: datetime

#     class Config:
#         orm_mode = True
