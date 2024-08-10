# Use the official Python image from the Docker Hub
FROM  --platform=linux/amd64 python:3.9-slim as build

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application files
COPY helloworld.py helloworld.py

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["python", "helloworld.py"]
