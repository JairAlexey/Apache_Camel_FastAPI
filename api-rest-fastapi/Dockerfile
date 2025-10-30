FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy seed CSV to data directory (optional, used to generate JSON at runtime)
RUN mkdir -p /app/data
COPY data/envios.csv /app/data/envios.csv

EXPOSE 8080

CMD ["sh", "-c", "python -m app.bootstrap && uvicorn app.main:app --host 0.0.0.0 --port 8080"]
