from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.logger import get_logger
from app.exceptions.repository import RecommendationRepositoryError

logger = get_logger(log_name="exception_handlers", log_folder="system")


async def recommendation_repository_exception_handler(
    request: Request, exc: RecommendationRepositoryError
) -> JSONResponse:

    logger.exception(f"Repository error while processing request: {request.url.path}")

    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
