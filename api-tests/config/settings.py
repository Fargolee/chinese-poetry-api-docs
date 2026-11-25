import os


BASE_URL = os.getenv("POETRY_API_BASE_URL", "http://localhost:1279").rstrip("/")
TIMEOUT = float(os.getenv("POETRY_API_TIMEOUT", "10"))
