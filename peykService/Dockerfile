# Stage 1: Build the project
FROM python:3.9 AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy the source code and necessary files to the container
COPY src/ .

# Install dependencies
RUN apt-get update && apt-get install -y build-essential
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Build the project
RUN python setup.py install

# Stage 2: Run the application in a lightweight container
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the built project from the previous stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app .

# Install necessary dependencies
RUN apt-get update && apt-get install -y libgcc1

# Expose the port on which your FastAPI application runs
EXPOSE 8080

# Start the FastAPI application
CMD ["python", "-m", "uvicorn", "peyk:app", "--host", "0.0.0.0", "--port", "8080"]
