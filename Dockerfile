FROM python:3.9 AS base

RUN mkdir /booking
WORKDIR /booking
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

RUN chmod a+x docker/*.sh
# RUN pip install gunicorn
# RUN pip install prometheus_fastapi_instrumentator

CMD ["gunicorn", "src.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind 0.0.0.0:8000"]
