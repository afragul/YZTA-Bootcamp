from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.logging_config import setup_logging
from database import init_db
from routers import auth, chat, cv, health, learning_plan, upload
from services.cv_parser import CVParseError
from services.cv_service import CVAnalysisError, InvalidCVError

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    init_db()
    logger.info("application started")
    yield
    logger.info("application shutdown")


app = FastAPI(
    title="AI Kariyer Asistani API",
    version="0.3.0",
    description="Backend cekirdek API - Hafta 3 orkestrasyon",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(CVParseError)
async def cv_parse_error_handler(_: Request, exc: CVParseError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(InvalidCVError)
async def invalid_cv_error_handler(_: Request, exc: InvalidCVError):
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.exception_handler(CVAnalysisError)
async def cv_analysis_error_handler(_: Request, exc: CVAnalysisError):
    logger.exception("cv analysis error")
    return JSONResponse(status_code=502, content={"detail": str(exc)})


app.include_router(health.router)
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(cv.router)
app.include_router(learning_plan.router)
app.include_router(chat.router)
