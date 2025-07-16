FROM python:3.11-slim AS base

# Create a non-root user
RUN addgroup --system fetcher && adduser --system --ingroup fetcher fetcher

FROM base AS builder
WORKDIR /app

# Install dependencies in a virtual environment, using pip cache
COPY --link requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m venv .venv && \
    .venv/bin/pip install -r requirements.txt

FROM base AS final
WORKDIR /app

# Copy app source and venv from builder
COPY --from=builder /app/.venv /app/.venv
COPY --link main.py run.sh tickers.json ./

# Set PATH to use venv
ENV PATH="/app/.venv/bin:$PATH"

# Ensure run.sh is executable
RUN chmod +x run.sh

USER fetcher

CMD ["sh", "run.sh"]