from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.core.supabase_client import supabase
from app.schemas.offer import OfferCreate, OfferResponse

#router = APIRouter(prefix="/offers", tags=["offers"])
router = APIRouter(tags=["Offers"])


# -----------------------------
# 🔹 Crear una nueva oferta
# -----------------------------
@router.post("/", response_model=OfferResponse)
def create_offer(payload: OfferCreate):
    data = payload.dict()

    # ✅ Verificar si el usuario existe
    try:
        user_check = supabase.table("users").select("id").eq("id", data["client_id"]).execute()
        if not user_check.data:
            # Si no existe, crearlo automáticamente
            supabase.table("users").insert({
                "id": data["client_id"],
                "name": f"Cliente {data['client_id'][:8]}",
                "email": f"auto_{data['client_id'][:8]}@example.com"
            }).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verificando/creando usuario: {e}")

    # ✅ Construir el payload de inserción
    insert_payload = {
        "client_id": data["client_id"],
        "title": data["title"],
        "description": data.get("description"),
        "area_m2": data.get("area_m2"),
        "budget_cop": data.get("budget_cop"),
    }

    # Si tiene ubicación, la añadimos
    if data.get("location"):
        insert_payload["location"] = data["location"]  # Ej: "SRID=4326;POINT(-74.0628 4.6486)"

    # ✅ Insertar en Supabase
    try:
        resp = supabase.table("offers").insert(insert_payload).execute()
        if not resp.data:
            raise HTTPException(status_code=400, detail="Error creando oferta")
        return resp.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de Supabase: {e}")


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
# 🔹 Buscar ofertas cercanas (RPC)
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
