#  Configuration variables such as database URLs, Redis settings, and other environment-specific settings.
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Real-Time News Aggregator"
    PROJECT_VERSION: str = "0.1.0"
    DATABASE_URL: str = "mysql+pymysql://root:incorrect@localhost:3306/news_aggregator"
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CACHE_EXPIRE_IN_SECONDS: int = 60 * 15  # 15 minutes
    NEWS_API_KEY: str = "your_news_api_key"

    class Config:
        env_file = ".env"

settings = Settings()
DATABASE_URL = 'mysql+pymysql://root:incorrect@localhost:3306/news_aggregator'
