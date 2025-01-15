# Build stage
FROM python:3.13 AS builder

# Install Poetry
RUN pip install poetry==1.8

# Set Poetry environment variables
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set working directory
WORKDIR /app

# Copy dependency files and install dependencies
COPY pyproject.toml poetry.lock ./
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

# Runtime stage
FROM python:3.13-slim AS runtime

# Set environment variables for the virtual environment
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Set log level
ENV PICTURAS_LOG_LEVEL=WARN

# Copy virtual environment from builder
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copy application code
COPY picturas_change_brightness_tool_ms ./picturas_change_brightness_tool_ms

# Set entrypoint
ENTRYPOINT ["python", "-m", "picturas_change_brightness_tool_ms.main"]
