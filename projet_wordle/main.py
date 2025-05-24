from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import routeur_api

application = FastAPI()

application.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:8000"],
    allow_credentials=True,
)

application.include_router(routeur_api, prefix="/jeu")
