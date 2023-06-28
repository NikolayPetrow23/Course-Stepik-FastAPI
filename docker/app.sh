#!/bin/bash

alembic upgrade 923d6a1020a5
alembic upgrade 9dfdefe4b317

gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
