FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY requirements-ml.txt .
RUN pip install --no-cache-dir -r requirements.txt -r requirements-ml.txt

COPY app/ ./app/
COPY uploads/ ./uploads/

EXPOSE 8000

ENV DEMO_MODE=false

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
