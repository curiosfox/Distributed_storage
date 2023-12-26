FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . /app/

# Specify the command to run your Python script
CMD ["python3", "client.py"]