# =====================================================================
# --- Builder Stage ---
# In this stage, we install all build-time dependencies and Python
# packages. The final image will not contain any of these tools.
# =====================================================================
FROM python:3.11-slim-bookworm as builder

# Set the working directory
WORKDIR /app

# Prevent Python from writing pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies required for building Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies into a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =====================================================================
# --- Final Stage ---
# This is the actual image that will be deployed. It's much smaller
# because it only contains the application code and the installed
# Python packages, not the build tools from the builder stage.
# =====================================================================
FROM python:3.11-slim-bookworm

# Set the working directory
WORKDIR /app

# Create a non-root user for security best practices
RUN addgroup --system app && adduser --system --group app

# Copy the virtual environment with installed packages from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application code
COPY . .

# Copy the entrypoint script and make it executable BEFORE switching user
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Change ownership of the app directory to the new user
RUN chown -R app:app /app

# --- Switch to the non-root user ---
USER app

# Set the path to include the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Expose the port Gunicorn will run on
EXPOSE 8000

# Set the entrypoint for the container
ENTRYPOINT ["/entrypoint.sh"]