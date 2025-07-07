from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time
from .logger import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log de la petición
        body = await request.body()
        logger.info(f"Request: {request.method} {request.url} Body: {body.decode('utf-8')}")

        # Ejecutar la respuesta
        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception(f"Exception during request: {str(e)}")
            raise

        process_time = time.time() - start_time
        logger.info(f"Response status: {response.status_code} (Processed in {process_time:.2f}s)")

        return response
