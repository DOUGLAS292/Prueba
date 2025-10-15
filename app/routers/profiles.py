from fastapi import APIRouter, HTTPException
from app.core.supabase_client import supabase
from app.schemas.profile import ProfileCreate, ProfileResponse

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.post("/register", response_model=ProfileResponse)
def register_user(profile: ProfileCreate):
    # 1. Crear usuario en auth de Supabase
    auth_response = supabase.auth.sign_up({
        "email": profile.email,
        "password": profile.password
    })
    if not auth_response.user:
        raise HTTPException(status_code=400, detail="Error al registrar usuario")

    user_id = auth_response.user.id

    # 2. Crear perfil en la tabla public.profiles
    data = {
        "id": user_id,
        "full_name": profile.full_name,
        "email": profile.email,
        "phone": profile.phone,
        "city": profile.city,
        
    
    }

    supabase.table("profiles").insert(data).execute()
    return data


@router.post("/login")
def login_user(email: str, password: str):
    auth_response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password
    })

    if not auth_response.user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return {
        "message": "Login exitoso",
        "user": {
            "id": auth_response.user.id,
            "email": auth_response.user.email
        },
        "access_token": auth_response.session.access_token
    }
