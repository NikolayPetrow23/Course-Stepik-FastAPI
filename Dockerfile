FROM python:3.9 AS base

RUN mkdir /booking
WORKDIR /booking
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN chmod a+x docker/*.sh
RUN chmod a+r prometheus.yml
RUN pip install gunicorn
RUN pip install prometheus_fastapi_instrumentator
#RUN chmod a+x data/data.json
#RUN chmod a+x src/static/*
#RUN apt-get update && apt-get install -y docker-compose

#CMD ["gunicorn", "src.main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind 0.0.0.0:8000"]