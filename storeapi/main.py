import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from storeapi.database import database
from storeapi.logging_conf import configure_logging
from storeapi.routers.post import router as post_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Hello world")
    logger.info("Hello world")
    logger.info("Hello world")
    logger.info("Hello world")
    # this function can run this
    await database.connect()
    #  and then it stops running until fastAPI tells it to continue and then it runs that.
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(post_router)
