import time

import psutil
from fastapi import Request
from loguru import logger


async def log_requests(request: Request, call_next: callable) -> any:
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = (time.perf_counter() - start_time) * 1000
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Duration: {process_time:.2f}ms"
    )

    return response


async def log_requests_development(request: Request, call_next: callable) -> any:
    process = psutil.Process()

    start_time = time.perf_counter()
    start_ram = process.memory_info().rss / 1024 / 1024  # Convert to MB

    response = await call_next(request)

    end_time = time.perf_counter()
    end_ram = process.memory_info().rss / 1024 / 1024  # Convert to MB

    duration = (end_time - start_time) * 1000  # Convert to ms
    ram_delta = end_ram - start_ram

    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Duration: {duration:.2f}ms - "
        f"RAM: {start_ram:.2f}MB → {end_ram:.2f}MB "
        f"(Δ {ram_delta:+.2f}MB)"
    )

    return response
