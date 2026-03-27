FROM python:3.11-slim

WORKDIR /app

# Install shared base dependencies + api-specific dependencies.
COPY shared/requirements-base.txt /tmp/requirements-base.txt
COPY api/requirements.txt /tmp/requirements-api.txt
RUN pip install --no-cache-dir -r /tmp/requirements-base.txt -r /tmp/requirements-api.txt

# Copy service code after dependencies.
COPY api/ /app

EXPOSE 8001

# Override APP_MODULE/HOST/PORT as needed.
CMD ["sh", "-c", "uvicorn ${APP_MODULE:-main:app} --host ${HOST:-0.0.0.0} --port ${PORT:-8001}"]
