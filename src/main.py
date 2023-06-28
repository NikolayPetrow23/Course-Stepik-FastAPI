import time

import aioredis as aioredis
import sentry_sdk
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from sqladmin import Admin

from src.admin.auth import authentication_backend
from src.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UserAdmin
from src.bookings.router import router as router_bookings
from src.config import settings
from src.database import engine
from src.hotels.rooms.router import router as router_rooms
from src.hotels.router import router as router_hotels
from src.images.router import router as router_images
from src.importer.router import router as router_importer
from src.logger import logger
from src.pages.router import router as router_pages
from src.prometheus.router import router as router_prometheus
from src.users.router import router as router_users

sentry_sdk.init(
    dsn="https://89811d19da244099a20389b3310d7155@o4505415939784704.ingest.sentry.io/4505415942537216",
    traces_sample_rate=1.0,
)

app = FastAPI(title="Course Stepik")

app.include_router(router_users)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)

app.include_router(router_pages)
app.include_router(router_images)

app.include_router(router_importer)

app.include_router(router_prometheus)

origins = [
    # 3000 - порт, на котором работает фронтенд на React.js
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


@app.on_event("startup")
def startup():
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")


app = VersionedFastAPI(
    app,
    version_format='{major}',
    prefix_format='/v{major}',
)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)

Instrumentator().instrument(app).expose(app)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

admin = Admin(
    app,
    engine,
    title="Admin bookings.com",
    authentication_backend=authentication_backend,
)

admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # При подключении Prometheus + Grafana подобный лог не требуется
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
