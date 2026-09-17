from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import Base, engine, get_db
from app.api.sites import router as sites_router
from app.models.site import WebSite
from app.models.check import CheckLog


Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME,version="1.0.0")
app.include_router(sites_router,prefix="/api/v1/sites",tags=["sites"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_boot():
    return {"status":"WebTracker API is running smoothly"}

@app.get("/metrics",response_class=PlainTextResponse)
def get_metrics(db: Session = Depends(get_db)):
    total_sites = db.query(WebSite).count()
    failed_checks = db.query(CheckLog).filter(CheckLog.status_code == 0).count()

    metrics_payload = (
        f"# HELP webtracker_total_sites cantidad de sitios en el monitor\n"
        f"# TYPE webtracker_total_sites gauge\n"
        f"webtracker_total_sites {total_sites}\n\n"

        f"# HELP webtracker_failed_checks_total Cantidad de fallos detectados\n"
        f"# TYPE webtracker_failed_checks_total counter\n"
        f"webtracker_failed_checks_total {failed_checks}\n"
    )
    return PlainTextResponse(metrics_payload)