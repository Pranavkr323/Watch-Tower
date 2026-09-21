import time
from fastapi import Request
import logging

logger = logging.getLogger(__name__)

async def TimerMiddleware(request: Request, call_next):

    start_time = time.perf_counter()
    response = await call_next(request)
    total_time = time.perf_counter() - start_time

    logger.info(
        "%s %s is complete in %.4f seconds",
        request.method,
        request.url.path,
        total_time
    )

    return response
