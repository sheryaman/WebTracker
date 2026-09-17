from fastapi import APIRouter , Depends , HTTPException
from sqlalchemy.orm import Session
from typing import List
import re

from app.core.database import get_db
from app.schemas.site import WebSiteCreate, WebSiteResponse
from app.crud import site as crud_site
from app.tasks import check_single_website

router = APIRouter()


def is_valid_url(url: str) -> bool:
    """Valida si una URL tiene un formato básico correcto"""
    pattern = re.compile(
        r'^(?:http|ftp)s?://'  
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # dominio
        r'localhost|'  
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(pattern, url) is not None

@router.post("/", response_model=WebSiteResponse,status_code=201)
def register_site(website:WebSiteCreate,db:Session = Depends(get_db)):
    try:
        
        if not is_valid_url(website.url):
            raise HTTPException(
                status_code=400, 
                detail="La URL proporcionada no tiene un formato válido"
            )
        
        
        if not website.name or len(website.name.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="El nombre del sitio no puede estar vacío"
            )
        
        new_site = crud_site.create_website(db=db,website=website)

        try:
            check_single_website(new_site.id)
        except Exception as e:
           print(f"Error al ejecutar check inmediatamente: {e}") 
        return new_site
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor al crear el sitio: {str(e)}"
        )

@router.get("/",response_model=List[WebSiteResponse])
def list_sites(db:Session = Depends(get_db)):
    try:
        return crud_site.get_websites(db=db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener la lista de sitios: {str(e)}"
        )

@router.delete("/{site_id}", status_code=204)
def delete_site(site_id: int, db: Session = Depends(get_db)):
    try:
        if site_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="El ID del sitio debe ser un número positivo"
            )
            
        site = crud_site.delete_website(db=db, site_id=site_id)
        if site is None:
            raise HTTPException(status_code=404, detail="Site not found")
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor al eliminar el sitio: {str(e)}"
        )