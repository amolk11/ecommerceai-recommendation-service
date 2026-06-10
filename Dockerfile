FROM python:3.12-slim

WORKDIR /app

COPY ecommerceai-recommendation-service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ecommerceai-platform-core /platform-core

RUN pip install /platform-core

COPY ecommerceai-recommendation-service/app ./app

COPY ecommerceai-recommendation-service/main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]