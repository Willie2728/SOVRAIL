FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY sovrail ./sovrail
RUN mkdir -p /data
ENV SOVRAIL_DB_PATH=/data/sovrail.db
CMD ["uvicorn","sovrail.main:app","--host","0.0.0.0","--port","8080"]
