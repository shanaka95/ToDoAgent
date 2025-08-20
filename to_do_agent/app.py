# Main FastAPI application for the ToDo Agent
# This is the entry point that sets up our web server and connects all the pieces together

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from to_do_agent.config.dependencies import get_app_settings
from to_do_agent.api.root_router import router as api_router
from fastapi.responses import JSONResponse
from to_do_agent.integrations.bubbletea.bubbletea_router import router as bubbletea_router
from mangum import Mangum
import uvicorn

# Load our app settings right at startup so we know how to configure everything
startup_app_settings = get_app_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function runs when our app starts up and shuts down.
    Think of it as the "on/off switch" for our application.
    """
    # When the app starts up, let's log some helpful info
    app_settings = get_app_settings()
    print(
        f"Starting {app_settings.service_name} service",
        f"Version: {app_settings.version}",
        f"Port: {app_settings.port}",
    )

    # This 'yield' means "keep the app running until it's time to shut down"
    yield


# Create our main FastAPI application
# This is like setting up the foundation of our house
app = FastAPI(
    title=startup_app_settings.service_name,
    description="To Do Agent",
    version=startup_app_settings.version,
    root_path="/prod/",  # This is for AWS Lambda deployment
    lifespan=lifespan,   # Connect our startup/shutdown handler
)
app.openapi_version = "3.0.2"

# Set up AWS Lambda handler for serverless deployment
# This lets us run our app on AWS without managing servers
handler = Mangum(app)

# Add CORS middleware to allow web browsers to talk to our API
# Without this, web apps couldn't call our API from different domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow requests from any website (for demo purposes)
    allow_credentials=True,     # Allow cookies and authentication headers
    allow_methods=["*"],        # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],        # Allow all request headers
)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    This is our safety net - if anything goes wrong, this function catches it
    and returns a nice error message instead of crashing the app.
    """
    print(f"Unhandled exception: {str(exc)}")

    # Return a user-friendly error response with timestamp
    return JSONResponse(
        status_code=500,
        content={
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": "internal_server_error",
            "message": "An internal server error occurred",
            "details": "Please try again later or contact support if the problem persists",
        },
    )


# Include our main API routes (this connects all our endpoints)
app.include_router(api_router)

# Include our BubbleTea router
app.include_router(bubbletea_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(startup_app_settings.port))
