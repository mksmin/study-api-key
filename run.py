import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting")
    yield
    print("stopping")


app = FastAPI(
    lifespan=lifespan,
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url=None,
)

if __name__ == '__main__':
    try:
        run_args = {
            "app": "run:app",
            "host": settings.run.host,
            "port": settings.run.port,
            "log_level": settings.run.log_level,
            "reload": settings.run.reload,
            "workers": settings.run.workers,
        }

        uvicorn.run(**run_args)
    except KeyboardInterrupt:
        print('stopping with KeyboardInterrupt')
    except Exception as e:
        print(e)
