FROM python:3.11-slim

WORKDIR /app

COPY ocr_worker.py .

RUN pip install boto3 pillow opencv-python-headless

CMD ["python", "ocr_worker.py"]
