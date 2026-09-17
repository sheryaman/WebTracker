from sqlalchemy import Column, Integer , String , Boolean , DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class WebSite(Base):
    __tablename__ = "web_sites"
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String, nullable=False)
    url = Column(String, index=True, nullable=False)
    check_interval = Column(Integer,default=60)
    is_active = Column(Boolean,default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())