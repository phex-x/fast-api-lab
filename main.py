from fastapi import FastAPI
from app.api.endpoints import router
from app.db.database import engine
from app.models.user import Base
import uvicorn
from redis import Redis
from dotenv import load_dotenv

load_dotenv()

redis_client = Redis(
    host='localhost',
    port=6379,
    db=0
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TSP API")

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
