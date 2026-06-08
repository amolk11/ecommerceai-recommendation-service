import time

from fastapi import Request

from app.core.logger import get_logger


logger = get_logger(log_name="request_timing", log_folder="middleware")


async def request_timing_middleware(request: Request, call_next):

    start_time = time.perf_counter()

    response = await call_next(request)

    duration_ms = (time.perf_counter() - start_time) * 1000
    
    response.headers["X-Process-Time"] = (f"{duration_ms:.2f}ms")

    logger.info(f"{request.method} {request.url.path} status={response.status_code} duration_ms={duration_ms:.2f}")

    return response
