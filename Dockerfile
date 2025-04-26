# syntax=docker/dockerfile:1.4
##################
# Stage 1: BUILDER
##################
FROM python:3.13-slim-bookworm AS build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /.venv
RUN pip install --user --no-cache-dir -r requirements.txt

COPY /app /app/

##################
# Stage 2: RUNTIME
##################
FROM python:3.13-slim-bookworm AS runtime

COPY --from=build /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

WORKDIR /app

COPY --from=build /root/.local /root/.local
COPY --from=build /app /app/

CMD ["python", "main.py"]




