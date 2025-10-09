from fastapi import APIRouter, HTTPException
from app.core.supabase_client import supabase
from app.schemas.profile import Profile

router = APIRouter()

@router.post("/", response_model=Profile)
def create_profile(profile: Profile):
    result = supabase.table("profiles").insert(profile.dict()).execute()
    if result.data:
        return result.data[0]
    raise HTTPException(status_code=400, detail=result.error_message)

@router.get("/{user_id}", response_model=Profile)
def get_profile(user_id: str):
    result = supabase.table("profiles").select("*").eq("id", user_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return result.data[0]
