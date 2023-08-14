from decouple import config
from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = config("CELERY_BROKER_URL")
celery.conf.result_backend = config("CELERY_RESULT_BACKEND")

celery.conf.imports = [
    config("CELERY_PATH_IMPORT")
]
