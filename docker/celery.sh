#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    celery --app=src.tasks.celery:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
    celery --app=src.tasks.celery:celery flower
fi