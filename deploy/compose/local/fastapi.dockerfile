FROM python:3.11.9-slim
EXPOSE 80

RUN apt-get update && \
	apt-get -y install make && \
	pip install poetry && \
	poetry config virtualenvs.create false && \
	poetry config installer.max-workers 10
COPY pyproject.toml poetry.lock  ./
RUN poetry install --no-root --no-interaction --no-ansi

COPY ./deploy /

RUN chmod +x /start-db-init.sh
RUN chmod +x /start-fastapi.sh
RUN chmod +x /start-reload-fastapi.sh
RUN chmod +x /start-celery-worker.sh
RUN chmod +x /start-celery-beat.sh
RUN chmod +x /entrypoint.sh

ADD ./src /src
WORKDIR /src
ENV PYTHONPATH=/src

ENTRYPOINT ["/entrypoint.sh"]
