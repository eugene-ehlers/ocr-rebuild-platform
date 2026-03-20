FROM python:3.11-slim

WORKDIR /app

COPY services/credit_decision/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

CMD ["python", "services/credit_decision/worker.py"]
