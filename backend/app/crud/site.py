from sqlalchemy.orm import Session
from app.models.site import WebSite
from app.models.check import CheckLog  

def get_websites(db: Session):

    sites = db.query(WebSite).all()
    

    for site in sites:
        last_check = (
            db.query(CheckLog)
            .filter(CheckLog.site_id == site.id)
            .order_by(CheckLog.created_at.desc())
            .first()
        )
        
        if last_check:
            site.last_status = last_check.status_code
            site.latency = last_check.response_time
        else:
            site.last_status = None
            site.latency = None
            
    return sites

def create_website(db: Session, website):
    db_obj = WebSite(name=website.name, url=website.url, check_interval=website.check_interval)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
def delete_website(db: Session, site_id: int):
    site = db.query(WebSite).filter(WebSite.id == site_id).first()
    if site:
        db.delete(site)
        db.commit()
    return site
