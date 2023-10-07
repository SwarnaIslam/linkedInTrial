# Use a Python base image
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the health-check script and any dependencies
COPY wait-for-rabbitmq.py .

# Install any Python dependencies if required
RUN pip install pika

# Specify the command to run when the container starts
CMD ["python", "wait-for-rabbitmq.py"]
