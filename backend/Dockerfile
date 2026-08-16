# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

# Update the OS and install dependencies
RUN apt-get update \
   && apt-get install -y --no-install-recommends \
      ca-certificates \
      wget \
      gpg \
   && wget https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb -O /tmp/packages-microsoft-prod.deb \
   && dpkg -i /tmp/packages-microsoft-prod.deb \
   && rm -f /tmp/packages-microsoft-prod.deb \
   && apt-get update \
   && apt-get install -y --no-install-recommends \
      libgdiplus \
      aspnetcore-runtime-8.0 \
   && apt-get upgrade -y \
   && apt-get purge --auto-remove -y \
   && apt-get autoremove --purge -y

# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Copy dependency files first to leverage Docker layer caching.
COPY pyproject.toml uv.lock ./

# Install the project's dependencies using the lockfile and settings.
RUN uv sync --locked --no-install-project

# Then, add the rest of the project source code and install it.
# Installing separately from its dependencies allows optimal layer caching.
COPY src /app/src
RUN uv sync --locked

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# Use the non-root user to run our application
USER nonroot

# Run the application with uvicorn
CMD uv run src/main_server.py
