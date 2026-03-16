FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY logo_worker.py .

CMD ["python", "logo_worker.py"]
