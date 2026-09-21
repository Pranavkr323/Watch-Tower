from fastapi import FastAPI
from app.routers import user_routes, monitor_routes
from app.Middleware.time_middleware import TimerMiddleware
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)

@app.get(
    "/",
    summary="API Home",
    description="Returns a welcome message to verify that the API is running.",
    tags=["General"],
)
def home():
    return {"success": "App is working!"}

app.middleware("http")(TimerMiddleware)
app.include_router(user_routes.router)
app.include_router(monitor_routes.router)
