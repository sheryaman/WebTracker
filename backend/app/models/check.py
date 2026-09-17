from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class CheckLog(Base):
    __tablename__ = "check_logs"
    id = Column(Integer,primary_key=True,index=True)
    site_id = Column(Integer,ForeignKey("web_sites.id",ondelete="CASCADE"),nullable=False)
    status_code = Column(Integer, nullable=True)
    response_time = Column(Float)
    ssl_valid = Column(Boolean)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),index=True)