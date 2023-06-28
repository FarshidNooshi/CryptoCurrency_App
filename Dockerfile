# Stage 1: Build the project
FROM python:3.9 as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential

# Copy requirements.txt and setup.py
COPY src/requirements.txt setup.py ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source src
COPY . .

# Build the project
RUN python -m compileall .
RUN python setup.py sdist bdist_wheel

# Stage 2: Create a lightweight image
FROM python:3.9-alpine

WORKDIR /app

# Copy the project from the previous stage
COPY --from=builder /app/dist/ /app/dist/

# Install the project and its dependencies
RUN pip install --no-cache-dir /app/dist/*.whl

# Set the entrypoint command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
