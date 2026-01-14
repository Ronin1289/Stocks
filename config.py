# Configuration for Prometheus web app.
#
# You can set `USERNAME` and `PASSWORD` here, or export
# `PROMETHEUS_USERNAME` and `PROMETHEUS_PASSWORD` as environment variables.
# For session signing you may set `FLASK_SECRET_KEY` here or via
# the `FLASK_SECRET_KEY` environment variable.

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env (project root)
basedir = Path(__file__).resolve().parent
load_dotenv(basedir / '.env')

# Sensible defaults (used if env vars are not set)
USERNAME = "Admin"
PASSWORD = "Flasky123$%^"
FLASK_SECRET_KEY = "super-duper-secret"

# Read from environment with sensible defaults
USERNAME = os.getenv('PROMETHEUS_USERNAME', USERNAME)
PASSWORD = os.getenv('PROMETHEUS_PASSWORD', PASSWORD)
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', FLASK_SECRET_KEY)
