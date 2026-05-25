FROM python:3.11-slim

LABEL maintainer="Syed Aun Ali Kazmi"
LABEL project="MLOps-Project3-K8s"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/app.py .
COPY src/ ./src/

EXPOSE 7000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s \
  CMD curl -f http://localhost:7000/health || exit 1

CMD ["python", "app.py"]
