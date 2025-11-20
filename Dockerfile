# 1. BASE IMAGE: Start from a small, stable Python image
FROM python:3.11-slim

# Set environment variables to ensure Python output is directed correctly
ENV PYTHONUNBUFFERED 1
ENV FASTAPI_PORT 8000
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. CODE: Copy the rest of the source code into the container
# This copies sql_app.py, .env, etc.
COPY . .

# 5. PORT: Inform the Docker environment that the app listens on this port
EXPOSE 8000

# 6. RUN COMMAND: Define the command that starts the web server
# We use Gunicorn (-w 4 for 4 worker processes) with Uvicorn workers,
# pointing to your main FastAPI instance.
#
# CRITICAL: 'sql_app' is the Python module (your file name minus .py),
# and 'app' is the FastAPI instance name (e.g., app = FastAPI()) inside that file.
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "sql_app:app"]
