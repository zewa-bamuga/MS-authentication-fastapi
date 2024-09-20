from celery import Celery

import app.domain
from app.containers import Container


def create_celery_app() -> Celery:
    container = Container()
    container.wire(packages=[app.domain])
    container.init_resources()

    return container.celery_app()


celery_app = create_celery_app()
