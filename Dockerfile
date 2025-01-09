# Use the official Python image from the Docker Hub
FROM python:3.11

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc fish git wget unzip libatomic1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install pipenv

# Set the working directory
WORKDIR /app

# Copy Pipfile and Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock ./

# Install Python dependencies using pipenv
RUN pipenv install --deploy --system

# Copy the rest of the application code to the working directory
COPY . .

# Entry point for the container
CMD ["fish"]
