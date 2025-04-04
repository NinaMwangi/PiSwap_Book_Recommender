# Stage 1: Build stage
FROM python:3.12 AS build

# Set the working directory
WORKDIR /app

# Copy dependencies first (leverages Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Stage 2: Final runtime image
FROM python:3.12-slim

WORKDIR /app

# Copy installed dependencies from the build stage
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=build /app /app

# Expose the FastAPI port
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "API.endpoints:app", "--host", "0.0.0.0", "--port", "7000"]
