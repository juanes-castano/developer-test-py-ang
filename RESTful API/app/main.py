from fastapi import FastAPI
from .routes import router
from .middleware import LoggingMiddleware

app = FastAPI(title="Medical Image Processing API")
app.add_middleware(LoggingMiddleware)
app.include_router(router)
