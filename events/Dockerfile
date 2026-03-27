# Azure Functions images are published for linux/amd64; on Apple Silicon (ARM) Docker
# must pull/run with explicit platform or the manifest lookup fails.
FROM --platform=linux/amd64 mcr.microsoft.com/azure-functions/python:4-python3.11

WORKDIR /home/site/wwwroot

# Install shared base dependencies + events-specific dependencies.
COPY shared/requirements-base.txt /tmp/requirements-base.txt
COPY events/requirements.txt /tmp/requirements-events.txt
RUN pip install --no-cache-dir -r /tmp/requirements-base.txt -r /tmp/requirements-events.txt

# Copy service code after dependencies.
COPY events/ /home/site/wwwroot

EXPOSE 80
