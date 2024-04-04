# Use a slim Python 3 image as the base
FROM python:3.9-slim

# Set the working directory for the container
WORKDIR /app

# Copy requirements.txt file
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Copy the entire project directory to the container
COPY . .
# Expose the Django development server port
EXPOSE 8000
# Run Django development server
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
