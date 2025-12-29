# Dockerfile

# Use a minimal Python image as the base
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Set the working directory in the container
WORKDIR /

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    curl libsnappy-dev make gcc g++ libc6-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*


FROM builder AS build1
# Copy only dependency files first (to leverage caching)
COPY pyproject.toml uv.lock ./

ENV UV_PROJECT_ENVIRONMENT=/usr/local
ENV UV_CONCURRENT_DOWNLOADS=8
# Install project dependencies using uv
RUN uv sync --extra inference

# Copy the rest of the application code
FROM builder AS build2
COPY --from=build1 /usr/local /usr/local
COPY . . 

# Expose the application port
EXPOSE 8000

# Run the application with uv
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
ENTRYPOINT ["python", "-m", "awslambdaric"]
CMD ["app.handler"]