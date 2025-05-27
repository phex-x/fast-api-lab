from fastapi import FastAPI
from app.api.endpoints import router
from app.db.database import engine
from app.models.user import Base
from redis import Redis
from dotenv import load_dotenv
import os

load_dotenv()

redis = Redis(
    host=os.getenv(),
    port=int(os.getenv()),
    db=int(os.getenv()),
    decode_responses=True
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TSP API")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
