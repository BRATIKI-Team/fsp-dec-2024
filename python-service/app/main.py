from sys import prefix

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import user_router, region_router, event_router, event_request_router


def get_application() -> FastAPI:
    application = FastAPI()

    #middlewares
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    #routes
    application.include_router(user_router.router, tags=["users"], prefix="/user")
    application.include_router(event_router.router, tags=["events"], prefix="/events")
    application.include_router(region_router.router, tags=["regions"], prefix="/regions")
    application.include_router(event_request_router.router, tags=["event-requests"], prefix="/event-requests")

    return application


app = get_application()
