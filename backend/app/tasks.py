import time
import requests
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

celery_app = Celery("app.tasks", broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0")

@celery_app.task(name='app.tasks.check_single_website')
def check_single_website(website_id: int):
    db = TestingSessionLocal()
    try:
        from app.models.site import WebSite
        from app.models.check import CheckLog

        site = db.query(WebSite).filter(WebSite.id == website_id).first()
        if not site or not site.is_active:
            return f"Sitio {website_id} inactivo o no encontrado."

        start_time = time.time()
        ssl_valid = site.url.startswith("https://")

        try:
            response = requests.get(site.url, timeout=10)
            status_code = response.status_code
        except requests.RequestException:
            status_code = 0  

        end_time = time.time()
        response_time = (end_time - start_time) * 1000

        log_entry = CheckLog(
            site_id=site.id,
            status_code=status_code,
            response_time=response_time,
            ssl_valid=ssl_valid
        )
        db.add(log_entry)
        db.commit()
        return f"Check en {site.url} - Status: {status_code} - {response_time:.2f}ms"
    finally:
        db.close()

@celery_app.task(name='app.tasks.discover_and_schedule_websites')
def discover_and_schedule_websites():
    db = TestingSessionLocal()
    try:
        from app.models.site import WebSite
        active_sites = db.query(WebSite).filter(WebSite.is_active == True).all()
        
        for site in active_sites:
            check_single_website.delay(site.id)
            
        return f"Orquestados {len(active_sites)} sitios para monitoreo."
    finally:
        db.close()


# Al final de backend/app/tasks.py
celery_app.conf.beat_schedule = {
    "run-monitor-every-minute": {
        "task": "app.tasks.discover_and_schedule_websites",
        "schedule": 60.0,
    }
}
