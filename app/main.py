from fastapi import FastAPI
from app.database import Base, engine
from app.routers import user_routes
from app.models import User, Monitor

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get(
    "/",
    summary="API Home",
    description="Returns a welcome message to verify that the AnimeDex API is running.",
    tags=["General"],
)
def home():
    return {"success": "App is working!"}

app.include_router(user_routes.router)
