from fastapi import FastAPI
from app.routers import profiles, offers

app = FastAPI(title="Conexión de Independientes")

app.include_router(profiles.router, prefix="/profiles", tags=["Profiles"])
app.include_router(offers.router, prefix="/offers", tags=["Offers"])

@app.get("/")
def root():
    return {"message": "API funcionando correctamente 🚀"}
