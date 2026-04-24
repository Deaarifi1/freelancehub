import time
import logging
from fastapi import Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            start_time = time.time()
            
            logger.info(f"→ {request.method} {request.url.path}")
            
            await self.app(scope, receive, send)
            
            duration = time.time() - start_time
            logger.info(f"← {request.method} {request.url.path} — {duration:.3f}s")
        else:
            await self.app(scope, receive, send)