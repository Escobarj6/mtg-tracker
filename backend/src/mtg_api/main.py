from fastapi import FastAPI

from mtg_api.routers import health

app = FastAPI(title="MTG Tracker API")
app.include_router(health.router)
