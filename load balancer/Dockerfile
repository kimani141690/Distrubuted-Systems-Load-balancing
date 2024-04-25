# Dockerfile for load balancer
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the load_balancer contents into the container at /app
COPY load_balancer.py /app

# Copy the consistent_hashing contents into the container at /app
COPY consistent_hashing.py /app

RUN pip install --no-cache-dir -r ../requirements.txt

CMD ["python", "load_balancer.py"]
