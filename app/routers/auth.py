from fastapi import APIRouter, HTTPException
from app.core.supabase_client import supabase
from app.schemas.profile import ProfileCreate, ProfileResponse
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=ProfileResponse)
def register_user(data: ProfileCreate):
    """
    Crea un usuario en Supabase Auth y su perfil en la tabla 'profiles'.
    """
    try:
        # 1️⃣ Crear usuario en Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password,
        })

        user = auth_response.user
        if not user:
            raise HTTPException(status_code=400, detail="Error al crear el usuario en Auth")

        # 2️⃣ Crear perfil asociado al usuario
        profile_data = {
            "id": user.id,
            "full_name": data.full_name,
            "role": data.role,
            "profession": data.profession,
            "city": data.city,
            "country": data.country,
            "bio": data.bio,
            "experience_years": data.experience_years,
            "phone": data.phone,
            "image_url": data.image_url,
            "rating_avg": data.rating_avg,
            "rating_count": data.rating_count,
            "created_at": datetime.utcnow().isoformat(),
        }

        result = supabase.table("profiles").insert(profile_data).execute()
        if not result.data:
            raise HTTPException(status_code=400, detail="Error al crear el perfil")

        return result.data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/login")
def login_user(credentials: dict):
    """
    Inicia sesión en Supabase Auth y devuelve el token + datos del usuario.
    """
    try:
        email = credentials.get("email")
        password = credentials.get("password")

        if not email or not password:
            raise HTTPException(status_code=400, detail="Correo y contraseña son obligatorios")

        # 1️⃣ Autenticar usuario
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})

        if not response.session:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        user = response.user

        # 2️⃣ Obtener perfil asociado
        profile = supabase.table("profiles").select("*").eq("id", user.id).execute()
        if not profile.data:
            raise HTTPException(status_code=404, detail="Perfil no encontrado")

        return {
            "access_token": response.session.access_token,
            "user": profile.data[0]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

