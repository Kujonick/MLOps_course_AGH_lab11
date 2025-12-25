# Dockerfile

# Use a minimal Python image as the base
FROM python:3.12-slim-bookworm AS builder

# Set the working directory in the container
WORKDIR /

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    curl libsnappy-dev make gcc g++ libc6-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*


FROM builder AS build1
RUN pip install uv
# Copy only dependency files first (to leverage caching)
COPY pyproject.toml uv.lock ./

ENV UV_PROJECT_ENVIRONMENT=/usr/local
ENV UV_CONCURRENT_DOWNLOADS=8
# Install project dependencies using uv
RUN uv sync

# Copy the rest of the application code
FROM builder AS build2
COPY --from=build1 /usr/local /usr/local
COPY . . 

# Expose the application port
EXPOSE 8000

# Run the application with uv
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]