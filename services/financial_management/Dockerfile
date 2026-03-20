FROM python:3.11-slim

WORKDIR /app

COPY services/financial_management/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

CMD ["python", "-m", "services.financial_management.worker"]
