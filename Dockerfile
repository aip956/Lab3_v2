
FROM python:3.8.10-slim

WORKDIR /app

COPY . /app

# RUN pip install -r requirements.txt
# Install packages in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt



# Make port 8080 available outside the container
EXPOSE 8080

# Define environment variable
ENV NAME World

# Run when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
