FROM python:3.9-slim

WORKDIR /app

RUN mkdir -p /app/static

COPY app.py /app/
COPY requirements.txt /app/
COPY static/swagger.json /app/static/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]