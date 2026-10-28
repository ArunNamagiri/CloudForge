FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY analyzer/ ./analyzer/
COPY sample_logs/ ./sample_logs/
COPY api.py .

EXPOSE 5002

CMD ["gunicorn", "--bind", "0.0.0.0:5002", "--workers", "2", "--timeout", "120", "api:app"]