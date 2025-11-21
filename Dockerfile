# 1. BASE IMAGE: Start from a small, stable Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV FASTAPI_PORT 8000
# Define the working directory inside the container
WORKDIR /app

# 2. DEPENDENCIES: Copy dependency file and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. SSL CERTIFICATE: Copy the TiDB CA certificate
# This file is crucial for the secure connection to TiDB Cloud.
COPY tidb_ca_cert.pem .

# 4. SSL ARGS: Set ENV variable for SQLAlchemy to find the certificate path
# Your Python code (database.py) MUST read this variable.
ENV SQLALCHEMY_CONNECT_ARGS '{"ssl": {"ca": "tidb_ca_cert.pem"}}'

# 5. CODE: Copy the rest of the source code into the container
COPY . .

# 6. PORT: Inform the Docker environment that the app listens on this port
EXPOSE 8000

# 7. RUN COMMAND: Define the command that starts the Uvicorn web server
# This uses the direct Uvicorn command, pointing to the standard entry file.
CMD ["uvicorn", "inventrack.main:app", "--host", "0.0.0.0", "--port", "8000"]
