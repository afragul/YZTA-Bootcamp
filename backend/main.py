from fastapi import FastAPI

from routers import health, upload

app = FastAPI(
    title="AI Kariyer Asistani API",
    version="0.1.0",
    description="Backend cekirdek API - Hafta 1 iskelet",
)

app.include_router(health.router)
app.include_router(upload.router)
