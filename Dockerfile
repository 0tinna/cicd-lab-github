FROM python:3.10-slim
ARG APP_VERSION=v1
ENV APP_VERSION=${APP_VERSION}
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/app.py .
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
