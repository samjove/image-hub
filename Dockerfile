# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

EXPOSE 8000

# Define environment variables (optional)
ENV DEBUG=True

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
