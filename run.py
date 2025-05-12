# import libs
import uvicorn

# import from libs
from contextlib import asynccontextmanager
from fastapi import FastAPI

# import from modules
from app.core.config import CustomFormatter, logger, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Start FastAPI APP")
    yield
    logger.info("Stop FastAPI APP")


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
        logger.info('stopping with KeyboardInterrupt')
    except Exception as e:
        logger.exception(e)
