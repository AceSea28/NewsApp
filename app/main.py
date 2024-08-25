from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.api_v1.endpoints import users, news
from app.db.base import Base
from app.db.session import engine
from app.models import user
from app.core.cache import redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    await redis_client.ping()
    yield
    # Shutdown
    await redis_client.close()

app = FastAPI(lifespan=lifespan)

# Include your routers
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(news.router, prefix="/api/v1", tags=["news"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)