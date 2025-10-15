from fastapi import APIRouter, HTTPException, Query, Depends, Header
from typing import Optional
from app.core.supabase_client import supabase
from app.schemas.offer import OfferCreate, OfferResponse
import requests

router = APIRouter(prefix="/offers", tags=["Offers"])

# 🔹 Dependencia para obtener el usuario actual desde el token
def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token de autorización no proporcionado")

    token = authorization.replace("Bearer ", "")
    # ✅ Llamamos a Supabase Auth para verificar el token y obtener el usuario
    try:
        resp = requests.get(
            f"{supabase.supabase_url}/auth/v1/user",
            headers={"Authorization": f"Bearer {token}", "apikey": supabase.supabase_key},
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")

        user = resp.json()
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verificando usuario: {e}")


# -----------------------------
# 🔹 Crear oferta (requiere login)
# -----------------------------
@router.post("/", response_model=OfferResponse)
def create_offer(payload: OfferCreate, user=Depends(get_current_user)):
    try:
        user_id = user["id"]

        # ✅ Verificar si el perfil existe
        profile_check = supabase.table("profiles").select("id").eq("id", user_id).execute()
        if not profile_check.data:
            raise HTTPException(status_code=404, detail="El perfil asociado no existe. Por favor crea tu perfil primero.")

        # ✅ Construir payload
        insert_payload = {
            "client_id": user_id,
            "title": payload.title,
            "description": payload.description,
            "area_m2": payload.area_m2,
            "budget_cop": payload.budget_cop,
            "location": payload.location,
        }

        # ✅ Insertar oferta
        resp = supabase.table("offers").insert(insert_payload).execute()
        if not resp.data:
            raise HTTPException(status_code=400, detail="Error creando oferta")
        return resp.data[0]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando oferta: {e}")


# -----------------------------
# 🔹 Listar ofertas recientes
# -----------------------------
@router.get("/")
def list_offers(limit: int = 50):
    try:
        resp = (
            supabase.table("offers")
            .select("*")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return resp.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo ofertas: {e}")


# -----------------------------
# 🔹 Buscar ofertas cercanas
# -----------------------------
@router.get("/nearby")
def offers_nearby(
    lon: float = Query(..., description="Longitud"),
    lat: float = Query(..., description="Latitud"),
    radius_m: int = Query(5000, description="Radio en metros"),
):
    try:
        resp = supabase.rpc(
            "offers_nearby", {"lon": lon, "lat": lat, "radius_m": radius_m}
        ).execute()

        if resp.data is None:
            raise HTTPException(status_code=404, detail="No se encontraron ofertas cercanas")

        return resp.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en RPC offers_nearby: {e}")
