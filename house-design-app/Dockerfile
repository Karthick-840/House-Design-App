FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY src/ ./src/

# Copy the tests into the container
COPY tests/ ./tests/

# Set the command to run the application (modify as needed)
CMD ["python", "-m", "src"]