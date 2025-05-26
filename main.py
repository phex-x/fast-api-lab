from fastapi import FastAPI
from app.api.endpoints import router
from app.db.database import engine
from app.models.user import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TSP API")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
