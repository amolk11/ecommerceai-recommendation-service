FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

COPY ecommerceai-recommendation-service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ecommerceai-recommendation-service/app ./app
COPY ecommerceai-recommendation-service/main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
