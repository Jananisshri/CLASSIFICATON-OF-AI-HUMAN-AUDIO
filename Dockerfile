# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies needed for librosa and audio processing
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port (Note: Railway will set the PORT environment variable)
EXPOSE 8000

# Command to run the application using shell form to support $PORT substitution
# We default to 8000 if PORT is not set
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
