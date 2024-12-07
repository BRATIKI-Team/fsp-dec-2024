from sys import prefix

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import user_router, region_router, event_router, event_request_router, file_router, \
    member_request_router, statistics_router

from app.api.routes import user_router, region_router, event_router, seeder_router


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
    application.include_router(user_router.router, tags=["users"], prefix="/users")
    application.include_router(event_router.router, tags=["events"], prefix="/events")
    application.include_router(region_router.router, tags=["regions"], prefix="/regions")
    application.include_router(event_request_router.router, tags=["event-requests"], prefix="/event-requests")
    application.include_router(seeder_router.router, tags=["seeders"], prefix="/seeders")
    application.include_router(file_router.router, tags=["files"], prefix="/files")
    application.include_router(member_request_router.router, tags=["member-requests"], prefix="/member-reqs")
    application.include_router(statistics_router.router, tags=["statistics"], prefix="/statistics")

    return application


app = get_application()
