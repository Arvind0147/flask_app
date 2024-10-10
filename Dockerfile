FROM python:3.9-slim

WORKDIR /flask_app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gnupg \
    curl \
    unixodbc \
    unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /flask_app
COPY . /flask_app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/theta-wave-400523-1ce6711951a9.json

EXPOSE 8081
CMD ["python", "app.py"]