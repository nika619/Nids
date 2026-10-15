# Lets `gunicorn app:app` find the Flask instance when run from the repo root.
from .app import app
