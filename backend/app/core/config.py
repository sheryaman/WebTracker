from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "WebTracker Api"

    POSTGRES_USER: str = "monitor_user"
    POSTGRES_PASSWORD: str = "secret123"
    POSTGRES_SERVER: str = "postgres-db"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "web_monitor"
    
    REDIS_HOST: str = "monitor_redis"
    REDIS_PORT: str = "6379"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
    @property
    def DATABASE_URL(self) -> str:
      return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()