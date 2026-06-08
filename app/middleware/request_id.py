import uuid

from fastapi import Request

from app.core.logger import get_logger


logger = get_logger(log_name="request_id", log_folder="middleware")


async def request_id_middleware(request: Request, call_next):

    request_id = uuid.uuid4().hex[:8]

    request.state.request_id = request_id

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id

    logger.info(f"request_id={request_id} method={request.method} path={request.url.path}")

    return response
