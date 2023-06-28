FROM python:3.9

RUN mkdir /booking

WORKDIR /booking

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /booking/docker/*.sh

RUN alembic upgrade 9dfdefe4b317

RUN alembic upgrade 923d6a1020a5

CMD ["gunicorn", "src.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
