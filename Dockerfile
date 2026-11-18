# Core API image (risk model, scenarios, verifier). No GPU, no deep learning.
# Build:  docker build -t lung-quit-coach .
# Run:    docker run -p 8000:8000 lung-quit-coach   ->  http://localhost:8000/docs
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app

# run as a non-root user
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
