# syntax=docker/dockerfile:1.4
##################
# Stage 1: BUILDER
##################
FROM python:3.13-slim-bookworm AS build

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -Ls https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy deps
COPY pyproject.toml uv.lock ./

# Copy application code from working directory into application's workdir
COPY . .

# Install Task CLI (Taskfile.dev)
RUN curl -sSL https://taskfile.dev/install.sh | sh \
  && mv ./bin/task /usr/local/bin/task \
  && rm -rf ./bin
# Check Task installation
RUN task

### 2. TESTS AND LINTING
FROM python:3.13-slim-bookworm AS test

# Aseta työskentelyhakemisto ja ympäristömuuttujat globaalisti
WORKDIR /app
ENV PYTHONPATH=/app

# Muut COPY-komennot pysyvät ennallaan
COPY --from=build /app /app
COPY --from=build /app/tests /tests
COPY --from=build /app/Taskfile.yml ./
COPY --from=build /root/.local/bin/uv /usr/local/bin/uv
COPY --from=build /usr/local/bin/task /usr/local/bin/task
COPY --from=build /app/pyproject.toml /app/uv.lock ./

# Asenna tarvittavat työkalut
RUN uv pip install --no-cache-dir pytest flake8

# Aja Task-komennot
RUN task
RUN task test
RUN task lint

########################
# 3. Production stage
########################
FROM python:3.12-slim-bookworm AS prod

# Määritä ympäristömuuttujat
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Määritä työskentelyhakemisto
WORKDIR /app

# Kopioi virtuaaliympäristö ja sovelluskoodi build-vaiheesta
COPY --from=build /app/.venv /app/.venv
COPY --from=build /app /app

# Asenna paketit, jotta skripti voi toimia
RUN pip install --no-cache-dir .

# Määritä oletuskomennot
ENTRYPOINT [ "timecli" ]

