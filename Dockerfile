# syntax=docker/dockerfile:1.4

##################
# Stage 1: BUILDER
##################
FROM python:3.13-slim-bookworm AS build

# Install system dependencies (curl for downloading, build-essential if any C extensions)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv Python package manager
RUN curl -Ls https://astral.sh/uv/install.sh | sh
# Add uv to PATH
ENV PATH="/root/.local/bin:$PATH" 

WORKDIR /app

# Copy project definition and lock files
COPY pyproject.toml uv.lock* ./
# Copy all application source code
COPY . .

# Install the application and its runtime dependencies into the system Python
# This also creates the 'timecli' script based on [project.scripts]
RUN uv pip install --system .

# Install Task CLI
RUN curl -sSL https://taskfile.dev/install.sh | sh \
  && mv ./bin/task /usr/local/bin/task \
  && rm -rf ./bin

# Check Task installation by running the default task
RUN task

########################
# Stage 2: TESTS
########################
FROM python:3.13-slim-bookworm AS test

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# For uv, if needed, or other shell tools
ENV PATH="/root/.local/bin:$PATH" 

WORKDIR /app

# Copy application code, tests, and Taskfile from the build stage
COPY --from=build /app/app /app/app
COPY --from=build /app/tests /app/tests
COPY --from=build /app/Taskfile.yml /app/Taskfile.yml
# For context if tasks need it
COPY --from=build /app/pyproject.toml /app/pyproject.toml 

# Copy the Task CLI binary from the build stage
COPY --from=build /usr/local/bin/task /usr/local/bin/task

# Install testing tools (pytest, flake8) globally
RUN pip install --no-cache-dir pytest flake8

# Set PYTHONPATH so Python can find the 'app' module for tests
ENV PYTHONPATH=/app

# Run tests and linters using Task
RUN task test
RUN task lint

########################
# Stage 3: PRODUCTION
########################
FROM python:3.13-slim-bookworm AS production

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# No need for uv's PATH here unless uv is used for runtime package management

WORKDIR /app

# Copy project definition (needed for installing the package)
COPY --from=build /app/pyproject.toml /app/pyproject.toml
# If you use uv.lock for production dependencies, copy it too
# COPY --from=build /app/uv.lock* ./

# Copy the application code from the build stage
COPY --from=build /app/app /app/app

# Install the application and its runtime dependencies globally from the copied source
# This makes the 'timecli' script available
RUN pip install --no-cache-dir .
# If using uv and have uv.lock for prod:
# RUN uv pip install --system --no-cache .

# Set the entrypoint for the container
ENTRYPOINT ["timecli"]
# You can add a default command if desired, e.g., CMD ["--help"]