install:
	poetry install

run:
	cp -f ./deploy/compose/local/docker-compose.yml docker-compose.yml && \
		cp -n .env.example .env && \
		docker-compose up -d --build --remove-orphans

run-mac:
	cp -f ./deploy/compose/local/docker-compose.yml docker-compose.yml && \
	cp -f .env.example .env && \
	docker-compose up -d --build --remove-orphans

stop:
	docker-compose down

migration:
	docker-compose -f ./deploy/compose/test/docker-compose.yml --project-directory . \
		run --rm fastapi_test alembic revision --autogenerate && \
		sudo chown -R $(USER):$(USER) ./src/alembic

migration-apply:
	docker-compose -f ./deploy/compose/test/docker-compose.yml --project-directory . \
		run --rm fastapi_test alembic upgrade head


migration-downgrade:
	docker-compose -f ./deploy/compose/test/docker-compose.yml --project-directory . \
		run --rm fastapi_test alembic downgrade -1

logs:
	docker-compose logs -f

# Format & Lint

isort:
	isort .

black:
	black .

# Unix
#---------
pyupgrade:
	pyupgrade `find ./src -name "*.py" -type f`
#---------

flake8:
	flake8 .

mypy:
	mypy .

pyright:
	pyright

format: isort pyupgrade black

lint: flake8 pyright

lint-all: flake8 mypy pyright

format-lint: format lint

poetry-make-format-lint:
	poetry run make format-lint

prepare: install poetry-make-format-lint