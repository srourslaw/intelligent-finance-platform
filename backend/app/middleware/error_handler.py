"""
Enhanced Error Handling and Logging Middleware

Provides:
- Structured error responses
- Request/response logging
- Performance monitoring
- Error tracking with stack traces
"""

import time
import traceback
import logging
import os
from pathlib import Path
from datetime import datetime
from typing import Callable
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# Create logs directory if it doesn't exist
LOGS_DIR = Path('logs')
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging
handlers = [logging.StreamHandler()]

# Only add file handler if we can write to disk
try:
    log_file = LOGS_DIR / 'app.log'
    handlers.append(logging.FileHandler(log_file))
except (OSError, PermissionError) as e:
    # On ephemeral filesystems (like Render), log to stdout only
    print(f"Warning: Could not create log file: {e}. Logging to stdout only.")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for comprehensive error handling and logging.

    Features:
    - Catches all unhandled exceptions
    - Logs request/response details
    - Measures request duration
    - Returns structured error responses
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate request ID
        request_id = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"

        # Log request start
        start_time = time.time()

        logger.info(
            f"[{request_id}] {request.method} {request.url.path} - "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )

        try:
            # Process request
            response = await call_next(request)

            # Calculate duration
            duration = (time.time() - start_time) * 1000  # milliseconds

            # Log response
            logger.info(
                f"[{request_id}] {request.method} {request.url.path} - "
                f"Status: {response.status_code} - Duration: {duration:.2f}ms"
            )

            # Add custom headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{duration:.2f}ms"

            return response

        except Exception as exc:
            # Calculate duration even on error
            duration = (time.time() - start_time) * 1000

            # Log error with stack trace
            logger.error(
                f"[{request_id}] {request.method} {request.url.path} - "
                f"ERROR: {str(exc)} - Duration: {duration:.2f}ms\n"
                f"Stack trace:\n{traceback.format_exc()}"
            )

            # Determine status code
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            error_type = "InternalServerError"

            if hasattr(exc, 'status_code'):
                status_code = exc.status_code
                error_type = exc.__class__.__name__

            # Return structured error response
            return JSONResponse(
                status_code=status_code,
                content={
                    "error": {
                        "type": error_type,
                        "message": str(exc),
                        "request_id": request_id,
                        "timestamp": datetime.utcnow().isoformat(),
                        "path": str(request.url.path)
                    }
                },
                headers={
                    "X-Request-ID": request_id,
                    "X-Response-Time": f"{duration:.2f}ms"
                }
            )


class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    """
    Middleware for monitoring slow requests and resource usage.

    Logs warnings for requests exceeding threshold.
    """

    SLOW_REQUEST_THRESHOLD_MS = 1000  # 1 second

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        response = await call_next(request)

        duration = (time.time() - start_time) * 1000

        # Log slow requests
        if duration > self.SLOW_REQUEST_THRESHOLD_MS:
            logger.warning(
                f"SLOW REQUEST: {request.method} {request.url.path} - "
                f"Duration: {duration:.2f}ms (threshold: {self.SLOW_REQUEST_THRESHOLD_MS}ms)"
            )

        return response


def setup_error_handling(app):
    """
    Setup error handling middleware for the FastAPI app.

    Usage:
        from app.middleware.error_handler import setup_error_handling
        setup_error_handling(app)
    """

    # Add middlewares (order matters - first added = last executed)
    app.add_middleware(PerformanceMonitoringMiddleware)
    app.add_middleware(ErrorHandlingMiddleware)

    logger.info("Error handling and performance monitoring middleware initialized")
