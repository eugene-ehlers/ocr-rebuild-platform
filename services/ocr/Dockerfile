FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/services/ocr
COPY . /app/services/ocr/

ENV PYTHONPATH=/app

CMD ["python", "-m", "services.ocr.ocr_worker"]
