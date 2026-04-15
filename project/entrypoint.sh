#!/bin/sh

# This script is the entrypoint for the Docker container.
# It prepares the Django application and then starts the Gunicorn server.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Database Migrations ---
# It's common to run migrations here for simplicity.
# In a large-scale production environment (like Kubernetes), it's often
# better to run migrations as a separate, one-off "job" before deploying
# the new application containers. This prevents multiple containers from
# trying to migrate the database at the same time during a rollout.
echo "Running database migrations..."
python manage.py migrate

# --- Collect Static Files ---
# Gathers all static files from your apps into a single directory
# so they can be served efficiently by a web server or CDN.
echo "Collecting static files..."
python manage.py collectstatic --noinput

# --- Custom Management Commands ---
# Run any other custom setup commands your app needs.
echo "Loading help documents..."
python manage.py load_help_docs

# --- Start the Application Server ---
# The 'exec' command is important. It replaces the shell process with
# the Gunicorn process. This allows Gunicorn to correctly receive signals
# (like SIGTERM for graceful shutdown) from the container runtime.
#
# IMPORTANT: Use the $PORT environment variable provided by Cloud Run.
# Default to 8000 if $PORT is not set (for local testing).
echo "Starting Gunicorn..."
exec gunicorn docmanager.wsgi:application --bind 0.0.0.0:${PORT:-8000}