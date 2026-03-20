FROM python:3.11-slim

WORKDIR /app

COPY services/fica_compliance/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

CMD ["python", "services/fica_compliance/worker.py"]
