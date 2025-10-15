from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import profiles, offers, auth

app = FastAPI(title="API Ventanería")

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o ["http://127.0.0.1:5500"] para frontend local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(auth.router)
app.include_router(profiles.router)
app.include_router(offers.router)
