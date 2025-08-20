from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from to_do_agent.config.dependencies import get_app_settings
from to_do_agent.api.root_router import router as root_router
from fastapi.responses import JSONResponse
import uvicorn
from bubbletea_endpoints import fastapi_config_handler, fastapi_chat_handler, ChatRequest

# Get settings for initial setup
startup_app_settings = get_app_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler - manages startup and shutdown events.
    """
    # Startup
    app_settings = get_app_settings()
    print(
        f"Starting {app_settings.service_name} service",
        f"Version: {app_settings.version}",
        f"Port: {app_settings.port}",
    )

    yield


app = FastAPI(
    title=startup_app_settings.service_name,
    description="To Do Agent",
    version=startup_app_settings.version,
    root_path="/prod/",
    lifespan=lifespan,
)
app.openapi_version = "3.0.2"
handler = Mangum(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handle all exceptions with consistent response format.
    """
    print(f"Unhandled exception: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": "internal_server_error",
            "message": "An internal server error occurred",
            "details": "Please try again later or contact support if the problem persists",
        },
    )


app.include_router(root_router)

@app.get("/config")
async def bubbletea_config():
    return fastapi_config_handler()

@app.post("/chat")
async def bubbletea_chat(req: ChatRequest):
    return await fastapi_chat_handler(req)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(startup_app_settings.port))
