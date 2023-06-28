# Stage 1: Build the project
FROM python:3.9-alpine as builder

WORKDIR /app

# Copy the source code files
COPY . /app

# Install build dependencies
RUN apk add build-base

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Build the project
RUN python -m compileall .

# Stage 2: Create a production-ready image
FROM python:3.9-alpine

WORKDIR /app

# Copy the built files from the previous stage
COPY --from=builder /app /app

# Install runtime dependencies
RUN apk add --no-cache libstdc++

# Expose the necessary port(s)
EXPOSE 8001

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
